from collections import deque

import requests
import json

from pydantic import BaseModel


def add_proxy(proxy_id, meta):
    # 向proxy-center中增加proxy节点，同时更新redis
    host, port = proxy_id.split(":")
    url = f'http://10.143.55.90:9381/api/proxies/{host}%3A{port}/'
    jmeta = json.dumps(meta)
    r = requests.post(url, data=jmeta)
    print(r.status_code)
    print(r.text)


def delete_proxy(proxy_id):
    host, port = proxy_id.split(":")
    url = f'http://10.143.55.90:9381/api/proxies/{host}%3A{port}/'
    r = requests.delete(url)
    print(r.text)


class RedialInfo(BaseModel):
    real_ip: str = None


if __name__ == '__main__':
    proxy_id = '2.2.2.2:2222'
    meta = {"host": "2.2.2.2", "port": 2222, "max_conn": 100}
    # add_proxy(proxy_id, meta)
    # delete_proxy("1.1.1.1:1111")
    meta = {}
    redial = RedialInfo()
    redial.real_ip = "111"
    print(redial)

