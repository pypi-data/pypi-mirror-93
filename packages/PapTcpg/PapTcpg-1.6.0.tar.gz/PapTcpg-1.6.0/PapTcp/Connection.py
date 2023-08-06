import json
from socketpool import ConnectionPool, TcpConnector
import socket
'''
调用tcp链接获取数据实现类
'''


class GetTcpGrpcData():
    _RPC_EOL = "\r\n\r\n"

    def __init__(self, host, port):
        self.host = host
        self.port = port


    def blocking(self, version, className, methodName, params=''):
        d = {"host": self.host, "port": self.port}
        self._sock = ConnectionPool(factory=TcpConnector).connection(**d)
        with self._sock as sock:
            req = {
                "jsonrpc": '2.0',
                "method": '{}::{}::{}'.format(version, className, methodName),
                "ext": [],
                # "params": params,
                "id": ''
            }
            if params:
                req['params'] = params
            # print(req)
            c = json.dumps(req) + self._RPC_EOL
            sock.send(c.encode())
            response = b''
            chunk = sock.recv(1024)

            while chunk:  # 循环接收数据，因为一次接收不完整
                response += chunk
                if chunk.decode("utf-8").find(self._RPC_EOL) != -1:
                    break
                chunk = sock.recv(1024)
        return json.loads(response.decode("utf-8").replace(self._RPC_EOL, ""))
