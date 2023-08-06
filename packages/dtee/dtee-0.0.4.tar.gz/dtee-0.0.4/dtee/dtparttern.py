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
from .dtrule import KeyMixin

logger = logging.getLogger(__name__)

class DTParttern(object):
    def __init__(self,parser,rules):
        assert isinstance(rules, (list, tuple, KeyMixin,)), "rule 参数必须是 list,tuple,KeyMixin类型"
        self._rules = rules
        self._parser = parser

    def _set_data(self,data):
        if isinstance(data,bytes):
            data = data.decode('utf-8','ignore')
        self._data = data

    def _rule_right(self):
        for keyrule in self._rules:
            if not keyrule.compare(self._data):
                return False
        else:
            return True

    def _parse(self):
        return self._parser.parse(self._data)

    def parse_data(self,data):
        self._set_data(data)
        if self._rule_right():
            return self._parse()
        else:
            return False
