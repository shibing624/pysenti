# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""

import os

pwd_path = os.path.abspath(os.path.dirname(__file__))

# 停用词
stopwords_path = os.path.join(pwd_path, 'data/stopwords.txt')
# 模型
sentiment_model_path = os.path.join(pwd_path, 'data/sentiment_model.pkl')
# 情感词典，包括积极词典、消极词典
sentiment_dict_path = os.path.join(pwd_path, 'data/sentiment_dict.txt')
# 连词词典
conjunction_dict_path = os.path.join(pwd_path, 'data/conjunction_dict.txt')
# 副词词典
adverb_dict_path = os.path.join(pwd_path, 'data/adverb_dict.txt')
# 否定词典
denial_dict_path = os.path.join(pwd_path, 'data/denial_dict.txt')

# model train
train_file_path = os.path.join(pwd_path, 'train.txt')
