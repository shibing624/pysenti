# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from sentiment_classifier import model_classifier

texts = ["苹果是一家伟大的公司",
         "土豆丝很好吃",
         "土豆丝很难吃"]
for i in texts:
    result = model_classifier.classify(i)
    print(i, result)
