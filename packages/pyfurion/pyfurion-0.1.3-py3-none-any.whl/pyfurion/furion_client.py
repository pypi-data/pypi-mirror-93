import logging


from pyfurion.config import ClientConf
from pyfurion.meta_bucket import MetaEvent, MetaBucketFacade
from pyfurion.snapshot import SnapshotProcess
from pyfurion.zookeeper import ZookeeperProcess

logger = logging.getLogger(__name__)

_namespace = 'furion'


class MetaListener():
    def meta_change(self, meta_evnet: MetaEvent):
        pass


class Client(MetaListener):
    def __init__(self, zk_host, config_groups, env, metachange_listeners):
        self.client_conf = ClientConf(zk_host, config_groups, env, _namespace)
        self._metachange_listeners = metachange_listeners
        self._meta_bucket_facade = MetaBucketFacade(self.client_conf)
        self._snapshop_process = SnapshotProcess(self.client_conf, self)
        self._zookeeper_process = ZookeeperProcess(self.client_conf, self)
        try:
            self._zookeeper_process.start()
        except Exception as e:
            logger.exception("furion metazookeeper Client启动异常")
            self.client_conf.recovery_mode = True
            self._snapshop_process.recovery()

    # def __getattr__(self, name: str) -> Any:
    #     return self.get(name)

    def get(self, meta_key, config_group=None, default=None):
        if not config_group:
            if len(self.client_conf.config_groups) == 1:
                config_group = self.client_conf.config_groups[0]
            else:
                raise RuntimeError('config_group can not be None if client inited by muti config_group')
        return self._meta_bucket_facade.get(config_group, meta_key) or default

    def meta_change(self, meta_event: MetaEvent):
        self._meta_bucket_facade.update(meta_event)
        self._snapshop_process.update(meta_event)
        self.dispatch_metaevent(meta_event)

    def dispatch_metaevent(self, meta_event: MetaEvent):
        if self._metachange_listeners:
            for meta_listener in self._metachange_listeners:
                meta_listener.meta_change(meta_event)
