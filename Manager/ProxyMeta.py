from pydantic import BaseModel, Schema


class ProxyMeta(BaseModel, object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._max_conn: int = 100

    @property
    def host(self):
        return self.host

    @property
    def port(self):
        return self.port

    @property
    def max_conn(self):
        return self.max_conn
