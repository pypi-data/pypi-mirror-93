.. dtee documentation master file, created by
   sphinx-quickstart on Thu Jan 28 16:11:38 2021.


dtee 文档
====================================
| dtee是一个解析工具。它借助tornado的异步特性，对TCP协议下的数据传输对象stream进行解析。

安装
::

   pip install dtee


快速使用

   1)创建dtee脚本文件 dtee_script_one.py  # 设置解析规则的脚本

::

   from dtee.dtrule import DTRule,DTParserRule

   # 关键字规则，用于同一协议实例，不同类型数据分类
   keyrules = (
      DTRule(17,20,'abc'),
   )

   # 解析规则，用于同一协议实例，解析stream出来的数据
   parserules = (
      DTParserRule(0, 8, 'LRKKJ'),
      DTParserRule(17, 20, 'DEV_type'),
      DTParserRegxRule(r'DEV_sn:(?P<DEV_sn>.*?);'),
   )

----

   2)使用dtee脚本的启动文件 server.py  # 使用tornado TCP服务端

::

    from tornado.ioloop import IOLoop
    from tornado.tcpserver import TCPServer
    from dtee.dtparttern import DTParttern
    from dtee.dtparser import DTParser
    from dtee.dtmanager import DTParserManager

    from .dtee_script_one import keyrules,parserules

    class DTCloudTcpServer(TCPServer):

        def __init__(self,dpm,*args,**kwargs):
            self.dpm = dpm
            super(DTCloudTcpServer, self).__init__(*args,**kwargs)

        async def handle_stream(self, stream, address):
            self.dpm.init_stream(stream, address)
            await self.dpm.run()

    async def handle_data(data):
        '''获取解析的数据进行处理'''
        print("result:%s" % data)

    if __name__ == '__main__':
        port = 8000

        dtparsermanager = DTParserManager(b'END')   # 数据结尾标识
        dtparser = DTParser(parserules)
        dtparttern = DTParttern(dtparser,keyrules)
        dtparsermanager.add_parttern(dtparttern)
        dtparsermanager.add_callback(handle_data)

        server = DTCloudTcpServer(dpm = dtparsermanager)
        server.listen(port)
        IOLoop.current().start()

----

   3)利用测试脚本执行测试 test.py # 使用tornado TCP客户端

::

    from tornado import ioloop, gen, iostream
    from tornado.tcpclient import TCPClient
    @gen.coroutine
    def Trans():
        stream = yield TCPClient().connect('localhost',8000)
        try:
            while True:
                DATA = "$LRKKJ$;DEV_type:abc;DEV_sn:def;END"
                yield stream.write(DATA.encode('utf-8'))

        except iostream.StreamClosedError:
            pass
    if __name__ == '__main__':
        ioloop.IOLoop.current().run_sync(Trans)

----

- 服务端控制台，执行结果

::

   result: {'LRKKJ': '$LRKKJ$;', 'DEV_type': 'abc', 'DEV_sn': 'def'}
