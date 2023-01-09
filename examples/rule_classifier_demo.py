# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""
import pysenti

if __name__ == '__main__':
    texts = [
        "这个电影真心很难看，大多数人都不喜欢，被骂很久，早就习惯了。",
        "苹果是一家伟大的公司",
        "土豆丝很好吃",
        "土豆丝很难吃"
    ]
    for i in texts:
        r = pysenti.classify(i)
        print(i, r['score'])
        print(r)
