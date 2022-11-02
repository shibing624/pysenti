# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

from pysenti.compat import strdecode
from pysenti.model_classifier import ModelClassifier
from pysenti.rule_classfier import RuleClassifier

__version__ = '0.1.8'

rule_classifier = RuleClassifier()
classify = rule_classifier.classify

