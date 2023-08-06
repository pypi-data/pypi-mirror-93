# python-nacos
### 声明
> 参考nacos-sdk-python项目改造
>
> https://github.com/nacos-group/nacos-sdk-python

### Usage
```python
from nacos import NacosUsage

SERVER_ADDRESSES = "127.0.0.1:8848"
NAMESPACE = "44b27ac4-60c1-43e7-8ac3-ed34108ca1aa"

params = {
    "servers": SERVER_ADDRESSES,
    "namespace": NAMESPACE,
    "service_name": "test.service",
    # "ip": "127.0.0.1",
    "port": 8080,
    "cluster_name": "testCluster",
    "weight": 1.0,
    "metadata": {},
    "enable": True,
    "healthy": True,
    "ephemeral": True,
}

usage = NacosUsage(debug=False, daemon=False, **params)

# 获取配置
conf = usage.get_config(data_id="test")
print("config: {}".format(conf))

# 注册实例
usage.register_instance()
```
