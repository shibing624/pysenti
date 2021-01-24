# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from codecs import open

r = set()
with open('pos_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        r.add(line)

sentiments = set()
with open('sentiment_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip().split()
        w = line[0]
        sentiments.add(w)

with open('pos', 'w', encoding='utf-8') as f:
    for i in r:
        if i not in sentiments:
            f.write(i + ' 2' + '\n')
