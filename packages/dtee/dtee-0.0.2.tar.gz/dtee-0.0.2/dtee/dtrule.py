#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 9:28
# @Author: SHAW
# @QQ:838705177
# -----------------------

import logging
import re
from abc import ABCMeta

logger = logging.getLogger(__name__)

class DTAbstractRule(metaclass=ABCMeta):

    def __hash__(self):
        raise NotImplementedError

    def __getattr__(self, item):
        raise NotImplementedError


class KeyMixin(metaclass=ABCMeta):

    def compare(self, data):
        raise NotImplementedError


class ParserMixin(metaclass=ABCMeta):

    def data2dict(self, data, dstdict):
        raise NotImplementedError


class DTRule(DTAbstractRule):
    def __init__(self,f,k,v):
        self._fkv=(f,k,v)
        super(DTRule, self).__init__()

    def __hash__(self):
        return hash(self._fkv)

    def __getitem__(self, item):
        return self._fkv[item]


class DTKeyRule(DTRule,KeyMixin):

    def __init__(self,start,end,value):
        super(DTKeyRule, self).__init__(start,end,value)

    def compare(self, data):
        return data[self[0]:self[1]] == self[2]

class DTParserRule(DTRule,ParserMixin):

    def __init__(self,start,end,field,flag=True):
        self.flag = flag
        super(DTParserRule, self).__init__(start,end,field)

    def data2dict(self, data, dstdict:dict):
        dstdict[self[2]]=data[self[0]:self[1]]


class DTRegxRule(DTAbstractRule):

    def __init__(self,r:str):
        self._r = r
        super(DTRegxRule, self).__init__()

    def __hash__(self):
        return hash(self._r)

    def __str__(self):
        return self._r


class DTKeyRegxRule(DTRegxRule,KeyMixin):

    def __init__(self,regpattern,value):
        self._value = value
        super(DTKeyRegxRule, self).__init__(regpattern)

    def compare(self, data):
        res = re.search(self._r, data)
        return res.group(1)==self._value

class DTParserRegxRule(DTRegxRule,ParserMixin):

    def __init__(self,r,flag=True):
        self.flag = flag
        super(DTParserRegxRule, self).__init__(r)
        self._init_f()

    def _init_f(self):
        assert "<" in self._r and ">" in self._r ,"Exception Occur:param 'r' need '<' and '>'!"
        self._f = self._r[self._r.find('<')+1:self._r.find('>')]

    def data2dict(self, data, dstdict:dict):
        res = re.search(self._r,data)
        dstdict.update(res.groupdict())

def test():
    dtr = DTKeyRegxRule(r'ss','ss')
    result = isinstance(dtr,KeyMixin)
    print("result:",result)

if __name__ == '__main__':
    test()