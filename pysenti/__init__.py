# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from . import config
from .compat import strdecode
from .model_classifier import ModelClassifier
from .rule_classfier import RuleClassifier

__version__ = '0.1.6'

rule_classifier = RuleClassifier()
classify = rule_classifier.classify

model_classifier = ModelClassifier(config.sentiment_model_path)
