# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from . import config
from .sentiment import Sentiment

__version__ = '0.1.1'

model = Sentiment(config.sentiment_model_path)
model.load()
classify = model.classify
