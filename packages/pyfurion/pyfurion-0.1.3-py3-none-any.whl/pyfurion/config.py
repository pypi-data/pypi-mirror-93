class ClientConf():
    def __init__(self, zk_host, config_groups, env, namespace):
        self.zk_host = zk_host
        self.config_groups = config_groups if isinstance(config_groups, (list, tuple)) else (config_groups,)
        self.env = env
        self.namespace = namespace
        self.recovery_mode = False
