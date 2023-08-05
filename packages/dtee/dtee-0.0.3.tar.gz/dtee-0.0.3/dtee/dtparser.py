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
from .dtrule import ParserMixin

logger = logging.getLogger(__name__)

class DTParser(object):
    def __init__(self,rules):
        assert isinstance(rules, (list, tuple, ParserMixin,)), "rule 参数必须是 list,tuple,DTRule,DTRegxRule类型"
        self._rules = rules

    def parse(self,data):
        tmpdict=dict()
        for rule in self._rules:
            if rule.flag:
                rule.data2dict(data,tmpdict)
        return tmpdict

