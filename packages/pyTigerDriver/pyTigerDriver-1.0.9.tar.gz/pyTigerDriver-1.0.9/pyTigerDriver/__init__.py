# -*- coding: utf-8 -*-

from .misc import ExceptionAuth
from .pyDriver import GSQL_Client, ExceptionRecursiveRet, ExceptionCodeRet,REST_Client, REST_ClientError


class Client():
    def __init__(self, server_ip="127.0.0.1", username="tigergraph", password="tigergraph", cacert=""
                 ,version="3.0.5", commit="",restPort="9000",gsPort="14240",protocol="https"
                 ,graph="MyGraph",token=""):
        self.Rest = REST_Client(server_ip=server_ip,protocol=protocol,restPort=restPort,token=token)
        self.Gsql = GSQL_Client(server_ip=server_ip, username=username, password=password, cacert=cacert
                           ,version=version, commit=commit,graph=graph,gsPort=gsPort,protocol=protocol)