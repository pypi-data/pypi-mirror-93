#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 9:28
# @Author: SHAW
# @QQ:838705177
# -----------------------

'''
    用来解析stream中的数据
'''

import logging
import traceback

from tornado.iostream import StreamClosedError

logger = logging.getLogger(__name__)

class DTParserManager(object):
    def __init__(self,eof=b'END'):
        self.EOF = eof.encode('utf-8') if isinstance(eof,str) else eof
        self._partterns = list()
        self._callback=None

    def init_stream(self,stream, address):
        self._stream = stream
        self._address = address

    async def run(self):
        try:
            while True:
                data = await self._stream.read_until(self.EOF)
                if data:break # 一次连接，只取第一条匹配的数据（默认客户端，一次连接只传一条数据）
            parseddata = self.data_parse(data)
            if self._callback:
                await self._callback(parseddata)
        except StreamClosedError:
            logger.warning("Lost client at host %s", self._address[0])
        except Exception as e:
            traceback.print_exc()
            logger.warning("Exception Occur:%s", e)

    def add_parttern(self,dataparttern):
        self._partterns.append(dataparttern)

    def data_parse(self,data):
        for parttern in self._partterns:
            data = parttern.parse_data(data)
            if data:
                return data
        return False

    def add_callback(self,callback=None):
        if callback:self._callback = callback
