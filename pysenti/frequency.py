# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""


class BaseProb(object):
    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 0

    def exists(self, key):
        return key in self.d

    def getsum(self):
        return self.total

    def get(self, key):
        if not self.exists(key):
            return False, self.none
        return True, self.d[key]

    def freq(self, key):
        return float(self.get(key)[1]) / self.total

    def samples(self):
        return self.d.keys()


class AddOneProb(BaseProb):
    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 1

    def add(self, key, value):
        self.total += value
        if not self.exists(key):
            self.d[key] = 1
            self.total += 1
        self.d[key] += value
