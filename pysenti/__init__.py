# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from . import config
from .model_classifier import ModelClassifier
from .rule_classfier import RuleClassifier

__version__ = '0.1.3'

rule_classifier = RuleClassifier()
classify = rule_classifier.classify

model_classifier = ModelClassifier(config.sentiment_model_path)
