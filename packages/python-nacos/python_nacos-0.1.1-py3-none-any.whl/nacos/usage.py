#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created By Murray(murray) on 2021/1/29 上午9:38
--------------------------------------------------
"""
import logging
import socket

from .client import NacosClient, DEFAULT_GROUP_NAME
from .timer import NacosTimerManager, NacosTimer

logger = logging.getLogger(__name__)


def host_ip():
    """获取本机IP"""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


class NacosUsage(object):
    def __init__(self, servers, namespace, service_name, port, data_id=None, debug=False, daemon=True, **kwargs):
        self.servers = servers
        self.namespace = namespace
        self.client = None
        # 注册实例
        self.service_name = service_name
        self.port = port
        self.ip = kwargs.get("ip") or host_ip()
        self.cluster_name = kwargs.get("cluster_name")
        self.group_name = kwargs.get("group_name", DEFAULT_GROUP_NAME)

        # Nocas配置
        self.data_id = data_id

        # 日志及线程设置
        self.debug = str(debug).lower() == 'true'
        self.daemon = str(daemon).lower() == 'true'

        self.kwargs = kwargs
        self._init()

    def _init(self):
        self.client = NacosClient(
            server_addresses=self.servers,
            namespace=self.namespace,
            **{k: v for k, v in self.kwargs.items() if k in [
                "endpoint", "ak", "sk", "username", "password", "proxies"
            ]}
        )
        # 开启debug
        if self.debug:
            self.client.set_debugging()

    def _register(self):
        try:
            is_ok = self.client.add_naming_instance(
                service_name=self.service_name,
                ip=self.ip,
                port=self.port,
                cluster_name=self.cluster_name,
                group_name=self.group_name,
                **{k: v for k, v in self.kwargs.items() if k in [
                    "weight", "metadata", "enable", "healthy", "ephemeral", "proxies"
                ]}
            )
            if is_ok:
                return True
            logger.debug("[NacosUsage._register] ip:%s, port:%s, service_name:%s, namespace:%s, "
                         "server response:%s" % (self.ip, self.port, self.service_name, self.namespace, is_ok))
        except (Exception,) as e:
            logger.error("[NacosUsage._register] ip:%s, port:%s, service_name:%s, namespace:%s, "
                         "server response:%s" % (self.ip, self.port, self.service_name, self.namespace, e))
        return False

    def _get_instance(self):
        try:
            _instance = self.client.get_naming_instance(
                service_name=self.service_name,
                ip=self.ip or host_ip(),
                port=self.port,
                cluster_name=self.cluster_name,
                group_name=self.group_name,
                **{k: v for k, v in self.kwargs.items() if k in [
                    "ephemeral"
                ]}
            )
            if _instance:
                return True
        except (Exception,) as e:
            logger.error("[NacosUsage._get_instance] ip:%s, port:%s, service_name:%s, namespace:%s, "
                         "server response:%s" % (self.ip, self.port, self.service_name, self.namespace, e))
        return False

    def _register_instance(self):
        if not self._get_instance():
            self._register()

    def _send_heartbeat(self):
        try:
            _heart = self.client.send_heartbeat(
                service_name=self.service_name,
                ip=self.ip or host_ip(),
                port=self.port,
                cluster_name=self.cluster_name,
                group_name=self.group_name,
                **{k: v for k, v in self.kwargs.items() if k in [
                    "weight", "metadata", "ephemeral"
                ]}
            )
            is_ok = _heart["clientBeatInterval"] > 0
            if is_ok:
                return True
            logger.debug("[NacosUsage._send_heartbeat] ip:%s, port:%s, service_name:%s, namespace:%s, "
                         "server response:%s" % (self.ip, self.port, self.service_name, self.namespace, _heart))
        except (Exception,) as e:
            logger.error("[NacosUsage._send_heartbeat] ip:%s, port:%s, service_name:%s, namespace:%s, "
                         "server response:%s" % (self.ip, self.port, self.service_name, self.namespace, e))
        return False

    def _heartbeat_result(self, data):
        if not data:
            logger.error("[Nacos._heartbeat_result] ip:%s, port:%s, service_name:%s, namespace:%s" % (
                self.ip, self.port, self.service_name, self.namespace))
        return data

    def register_instance(self):
        self._register_instance()
        timer_manager = NacosTimerManager()
        instance_timer = NacosTimer(
            name="nacos_service_instance",
            fn=self._register_instance,
            interval=60,
            daemon=self.daemon
        )
        heartbeat_timer = NacosTimer(
            name="nacos_heardbeat",
            fn=self._send_heartbeat,
            interval=5,
            daemon=self.daemon
        )
        heartbeat_timer.set_on_result(self._heartbeat_result)
        timer_manager.add_timer(instance_timer)
        timer_manager.add_timer(heartbeat_timer)
        timer_manager.execute()

    def get_config(self, data_id=None, group=None, timeout=None, no_snapshot=None, use_failover=True):
        try:
            data_id = data_id or self.data_id
            group = group or self.group_name
            timeout = timeout or self.kwargs.get("timeout")
            _config = self.client.get_config(
                data_id=data_id,
                group=group,
                timeout=timeout,
                no_snapshot=no_snapshot,
                use_failover=use_failover
            )
            return _config
        except (Exception,) as e:
            logger.error("[NacosUsage._get_config] data_id:%s, group:%s, timeout:%s, namespace:%s, "
                         "server response:%s" % (data_id, group, timeout, self.namespace, e))
            raise e

    def publish_config(self, content, data_id=None, group=None, conf_type='txt', timeout=None):
        try:
            data_id = data_id or self.data_id
            group = group or self.group_name
            timeout = timeout or self.kwargs.get("timeout")
            _config = self.client.publish_config(
                data_id=data_id,
                group=group,
                content=content,
                conf_type=conf_type,
                timeout=timeout,
            )
            return _config
        except (Exception,) as e:
            logger.error("[NacosUsage.publish_config] data_id:%s, group:%s, timeout:%s, namespace:%s, "
                         "server response:%s" % (data_id, group, timeout, self.namespace, e))
            raise e
