# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py
   Description :
   Author :       JHao
   date：          2016/12/3
-------------------------------------------------
   Change Activity:
                   2016/12/3:
-------------------------------------------------
"""
import json

import requests

__author__ = 'JHao'

import random

from Util import EnvUtil
from DB.DbClient import DbClient
from Config.ConfigGetter import config
from Util.LogHandler import LogHandler
from Util.utilFunction import verifyProxyFormat
from ProxyGetter.getFreeProxy import GetFreeProxy


class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self):
        self.db = DbClient()
        self.raw_proxy_queue = 'raw_proxy_test'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy_test'

    def refresh(self):
        """从已有站点上抓取proxy，并存放到redis raw_proxy
        fetch proxy into Db by ProxyGetter/getFreeProxy.py
        :return:
        """
        max_conn = 100
        meta: dict = {}
        self.db.changeTable(self.raw_proxy_queue)
        for proxyGetter in config.proxy_getter_functions:
            # fetch
            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
                    # 直接存储代理, 不用在代码中排重, hash 结构本身具有排重功能
                    proxy = proxy.strip()
                    if proxy and verifyProxyFormat(proxy):
                        self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
                        host, port = proxy.split(":")
                        meta["host"] = host
                        meta["port"] = port
                        meta["max_conn"] = max_conn
                        self.db.put(proxy, json.dumps(meta))
                    else:
                        self.log.error('{func}: fetch proxy {proxy} error'.format(func=proxyGetter, proxy=proxy))
            except Exception as e:
                self.log.error(e)
                self.log.error("{func}: fetch proxy fail".format(func=proxyGetter))
                continue

    def get(self):
        """
        return a useful proxy
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if item_dict:
            if EnvUtil.PY3:
                return random.choice(list(item_dict.keys()))
            else:
                return random.choice(item_dict.keys())
        return None
        # return self.db.pop()

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool as list
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if EnvUtil.PY3:
            return list(item_dict.keys()) if item_dict else list()
        return item_dict.keys() if item_dict else list()

    def getNumber(self):
        self.db.changeTable(self.raw_proxy_queue)
        total_raw_proxy = self.db.getNumber()
        self.db.changeTable(self.useful_proxy_queue)
        total_useful_queue = self.db.getNumber()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}

    def add_proxy(proxy, meta):
        # 向proxy-center中增加proxy节点，同时更新redis
        host, port = proxy.split(":")
        url = f'http://10.143.55.90:9381/api/proxies/{host}%3A{port}/'
        jmeta = json.dumps(meta)
        r = requests.post(url, data=jmeta)
        # print(r.status_code)
        print(r.text)

    def delete_proxy(proxy):
        # 从proxy-center中删除proxy节点，同时更新redis
        host, port = proxy.split(":")
        url = f'http://10.143.55.90:9381/api/proxies/{host}%3A{port}/'
        r = requests.delete(url)
        # print(r.text)


if __name__ == '__main__':
    pp = ProxyManager()
    pp.refresh()
