# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description:
"""

import os

pwd_path = os.path.abspath(os.path.dirname(__file__))

# 停用词
stopwords_path = os.path.join(pwd_path, 'data/stopwords.txt')
# 模型
sentiment_model_path = os.path.join(pwd_path, 'data/sentiment_model.pkl')

# 短语情感词典
phrase_dict_path = os.path.join(pwd_path, 'data/phrase_dict.txt')
# 积极词典
positive_dict_path = os.path.join(pwd_path, 'data/positive_dict.txt')
# 消极词典
negative_dict_path = os.path.join(pwd_path, 'data/negative_dict.txt')
# 连词词典
conjunction_dict_path = os.path.join(pwd_path, 'data/conjunction_dict.txt')
# 标点词典
punctuation_dict_path = os.path.join(pwd_path, 'data/punctuation_dict.txt')
# 副词词典
adverb_dict_path = os.path.join(pwd_path, 'data/adverb_dict.txt')
# 否定词典
denial_dict_path = os.path.join(pwd_path, 'data/denial_dict.txt')
