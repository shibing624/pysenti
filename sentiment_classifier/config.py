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
