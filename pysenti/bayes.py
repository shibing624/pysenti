# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
from math import log, exp

from pysenti.frequency import AddOneProb
from pysenti.utils import dump_pkl, load_pkl


class Bayes(object):
    def __init__(self):
        self.d = {}
        self.total = 0

    def save(self, fname):
        d = {'total': self.total, 'd': {}}
        for k, v in self.d.items():
            d['d'][k] = v.__dict__
        dump_pkl(d, fname)

    def load(self, fname):
        d = load_pkl(fname)
        self.total = d['total']
        self.d = {}
        for k, v in d['d'].items():
            self.d[k] = AddOneProb()
            self.d[k].__dict__ = v

    def train(self, data):
        for d in data:
            c = d[1]
            if c not in self.d:
                self.d[c] = AddOneProb()
            for word in d[0]:
                self.d[c].add(word, 1)
        self.total = sum(map(lambda x: self.d[x].getsum(), self.d.keys()))

    def classify(self, x):
        tmp = {}
        for k in self.d:
            tmp[k] = log(self.d[k].getsum()) - log(self.total)
            for word in x:
                tmp[k] += log(self.d[k].freq(word))
        ret, prob = 0, 0
        for k in self.d:
            now = 0
            try:
                for otherk in self.d:
                    now += exp(tmp[otherk] - tmp[k])
                now = 1 / now
            except OverflowError:
                now = 0
            if now > prob:
                ret, prob = k, now
        return ret, prob
