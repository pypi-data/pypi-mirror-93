import json
import os


from pyfurion.config import ClientConf
from pyfurion.meta_bucket import MetaEvent, MetaEventType


class SnapshotProcess():
    def __init__(self, client_conf: ClientConf, meta_listener):
        self.root_dir = os.getenv('HOME', os.getcwd())
        self.meta_listener = meta_listener
        self.client_conf = client_conf
        for config_group in client_conf.config_groups:
            snapshot_path = self.get_snapshot_dir_path(config_group)
            if not os.path.exists(snapshot_path):
                os.makedirs(snapshot_path)

    def get_snapshot_dir_path(self, config_group):
        return f'{self.root_dir}/.{self.client_conf.namespace}/snapshot/{config_group}'

    def get_snapshot_meta_path(self, config_group, meta_key):
        return f'{self.get_snapshot_dir_path(config_group)}/{meta_key}.snapshot.json'

    def update(self, meta_event: MetaEvent):
        if self.client_conf.recovery_mode and meta_event.event_type == MetaEventType.INIT:
            return
        if meta_event.event_type != MetaEventType.DELETE:
            with open(self.get_snapshot_meta_path(meta_event.config_group, meta_event.meta_key), 'w') as f:
                f.write(json.dumps({
                    # 'id': meta_event.id,
                    'namespace': meta_event.namespace,
                    'configGroup': meta_event.config_group,
                    'metaKey': meta_event.meta_key,
                    'metaValue': meta_event.meta_value,
                    # 'version': meta_event.version,
                }))

    def recovery(self):
        for config_group in self.client_conf.config_groups:
            path = self.get_snapshot_dir_path(config_group)
            files = os.listdir(path)
            for file_name in files:
                index = file_name.rindex(".snapshot.json")
                if index < 0:
                    continue
                meta_key = file_name[:index]
                with open(f'{path}/{file_name}', 'r') as f:
                    meta_data = json.loads(f.read())
                    metaEvent = MetaEvent(self.client_conf.env, MetaEventType.INIT, self.client_conf.namespace,
                                          config_group, meta_key, meta_data['metaValue'])
                    self.dispatch_event(metaEvent)

    def dispatch_event(self, metaEvent: MetaEvent):
        self.meta_listener.meta_change(metaEvent)
