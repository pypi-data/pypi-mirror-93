import logging

from kazoo.client import KazooClient
from kazoo.protocol.states import (
    EventType)

from pyfurion import meta_path_util
from pyfurion.config import ClientConf
from pyfurion.meta_bucket import MetaEvent, MetaEventType

logger = logging.getLogger(__name__)


class ZookeeperProcess():
    def __init__(self, conf: ClientConf, meta_listener):
        self.conf = conf
        self.meta_listener = meta_listener
        self.sessionTimeoutMs = 15000
        self.connectionTimeoutMs = 15000
        self.baseSleepTimeMs = 1000
        self.maxRetries = 5
        self.zk = KazooClient(hosts=self.conf.zk_host)
        self.group_children = {}

    def start(self):
        self.zk.start()

        def data_watcher(event):
            logger.info(f'new event:{event}')
            _, namespace, env, config_group, meta_key = event.path.split('/')
            value = self.zk.get(event.path, watch=data_watcher)
            if value:
                value = value[0].decode()
            metaEvent = MetaEvent(self.conf.env, MetaEventType.INIT, namespace, config_group, meta_key, value)
            if event.type == EventType.CREATED:
                metaEvent.event_type = MetaEventType.ADD
            elif event.type == EventType.CHANGED:
                metaEvent.event_type = MetaEventType.UPDATE
            elif event.type == EventType.DELETED:
                metaEvent.event_type = MetaEventType.DELETE
            else:
                return
            self.dispatch_event(metaEvent)

        def init_child(config_group, name):
            path = meta_path_util.toPath(self.conf.env, self.conf.namespace, config_group, name)
            value = self.zk.get(path, watch=data_watcher)
            if value:
                value = value[0].decode()
            metaEvent = MetaEvent(self.conf.env, MetaEventType.INIT, self.conf.namespace,
                                  config_group, name, value)
            self.dispatch_event(metaEvent)

        for config_group in self.conf.config_groups:
            group = meta_path_util.group(self.conf.env, self.conf.namespace, config_group)
            self.zk.ensure_path(group)

            @self.zk.ChildrenWatch(group, send_event=True)
            def children_watcher(children, event):
                logger.info(f'children changed, new:{children},{event}')
                if not event:
                    return
                config_group = event.path[event.path.rindex('/') + 1:]
                # children = self.zk.get_children(e.path)
                current_children = self.group_children.get(config_group, [])
                added = set(children) - set(current_children)
                if added:
                    current_children.extend(added)
                    self.group_children[config_group] = current_children
                    for name in added:
                        init_child(config_group, name)

            children = self.zk.get_children(group)
            self.group_children[config_group] = children
            for name in children:
                init_child(config_group, name)

            logger.info(f"furion 开始监听path：{group}")
            logger.info(f"furion 初始化数据个数为：{len(children)}")

    def dispatch_event(self, metaEvent: MetaEvent):
        self.meta_listener.meta_change(metaEvent)
