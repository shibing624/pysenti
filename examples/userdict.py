# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

import os

from pysenti import RuleClassifier

d = RuleClassifier()
pwd_path = os.path.abspath(os.path.dirname(__file__))
d.load_user_sentiment_dict(pwd_path + '/../extra_dict/user_sentiment_dict.txt')
print(d.user_sentiment_dict)

a_sentence = ['剁椒鸡蛋好难吃。绝对没人受得了',
              '土豆丝很好吃', '土豆丝很难吃',
              '这笔钱是个天文数字',
              '啥也不是',
              '我一会儿出去玩了，你吃啥？给你带,然而你不知道']
for i in a_sentence:
    r = d.classify(i)
    print(i, r['score'])
    print(r)

