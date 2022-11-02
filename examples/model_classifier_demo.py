# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from pysenti import ModelClassifier

texts = ["苹果是一家伟大的公司",
         "土豆丝很好吃",
         "垃圾，在酒店中应该是很差的！",
         "我们刚走过一个烧烤店",
         "土豆丝很难吃"]

if __name__ == '__main__':
    m = ModelClassifier()
    for i in texts:
        r = m.classify(i)
        print(i, r)
