import enum
import logging

from pyfurion.config import ClientConf

logger = logging.getLogger(__name__)


class MetaEventType(enum.Enum):
    INIT = 1
    ADD = 2
    UPDATE = 3
    DELETE = 4


class MetaEvent():
    def __init__(self, env, event_type, namespace, config_group, meta_key, meta_value):
        self.env = env
        self.event_type = event_type
        self.namespace = namespace
        self.config_group = config_group
        self.meta_key = meta_key
        self.meta_value = meta_value


class MetaBucket():
    _storage = {}

    def get(self, meta_key: str):
        return self._storage.get(meta_key)

    def set(self, meta_key: str, meta_value: str):
        self._storage[meta_key] = meta_value

    def delete(self, meta_key: str):
        self._storage.pop(meta_key)


class MetaBucketFacade():
    _config_group_metabucket = {}

    def __init__(self, client_conf: ClientConf):
        for config_group in client_conf.config_groups:
            self.add_bucket(config_group, MetaBucket())

    def add_bucket(self, config_group, meta_bucket):
        self._config_group_metabucket[config_group] = meta_bucket

    def get_bucket(self, config_group) -> MetaBucket:
        return self._config_group_metabucket.get(config_group)

    def update(self, meta_event: MetaEvent):
        config_group = meta_event.config_group
        meta_bucket = self.get_bucket(config_group)
        if not config_group:
            return
        if meta_event.event_type in (MetaEventType.INIT, MetaEventType.UPDATE, MetaEventType.ADD):
            meta_bucket.set(meta_event.meta_key, meta_event.meta_value)
        elif meta_event.event_type == MetaEventType.DELETE:
            meta_bucket.delete(meta_event.meta_key, meta_event.meta_value)
        else:
            logger.warn(f'UNKNOW meta_event:{meta_event}')

    def get(self, config_group, meta_key):
        meta_bucket = self.get_bucket(config_group)
        if not config_group:
            return
        return meta_bucket.get(meta_key)
