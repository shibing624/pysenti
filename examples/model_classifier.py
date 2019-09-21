# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""


from sentiment_classifier import model_classifier

a_sentence = ['剁椒鸡蛋好难吃。绝对没人受得了',
              '土豆丝很好吃', '土豆丝很难吃',
              '这笔钱是个天文数字',
              '我一会儿出去玩了，你吃啥？给你带,然而你不知道']
for i in a_sentence:
    result = model_classifier.classify(i)
    print(i, result)
