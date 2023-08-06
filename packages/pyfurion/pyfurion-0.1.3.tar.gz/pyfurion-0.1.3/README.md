# Furion配置中心python客户端

## Qucik Start
### Install
```
pip install pyfurion
```
### How to use
```
from pyfurion import Client  
client = Client(zk_host, config_groups, env, metachange_listeners)
mysql_host = client.get('mysql_host')
```