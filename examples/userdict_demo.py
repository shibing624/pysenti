# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

from pysenti import RuleClassifier

if __name__ == '__main__':
    m = RuleClassifier()
    m.load_user_sentiment_dict('user_sentiment_dict.txt')
    print(m.user_sentiment_dict)

    a_sentences = ['剁椒鸡蛋好难吃。绝对没人受得了',
                   '土豆丝很好吃', '土豆丝很难吃',
                   '这笔钱是个天文数字',
                   '啥也不是',
                   '我一会儿出去玩了，你吃啥？给你带,然而你不知道']
    for i in a_sentences:
        r = m.classify(i)
        print(i, r['score'])
