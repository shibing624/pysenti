# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from .bayes import Bayes
from .tokenizer import segment
from .utils import filter_stop


class Sentiment(object):
    def __init__(self, model_path):
        self.classifier = Bayes()
        self.model_path = model_path

    def save(self):
        self.classifier.save(self.model_path)

    def load(self):
        self.classifier.load(self.model_path)

    def handle(self, doc):
        words = segment(doc)
        words = filter_stop(words)
        return words

    def train(self, neg_docs, pos_docs):
        data = []
        for sent in neg_docs:
            data.append([self.handle(sent), 'neg'])
        for sent in pos_docs:
            data.append([self.handle(sent), 'pos'])
        self.classifier.train(data)

    def classify(self, sent):
        """
        classifiy sentence text
        :param sent: text, str
        :return:    "positive_prob": 0.0,
                    "negative_prob": 0.0
                    dict
        """
        result = {"positive_prob": 0.0, "negative_prob": 0.0}
        ret, prob = self.classifier.classify(self.handle(sent))
        if ret == 'pos':
            result["positive_prob"] = round(prob, 3)
            result["negative_prob"] = round(1 - prob, 3)
        elif ret == 'neg':
            result["positive_prob"] = round(1 - prob, 3)
            result["negative_prob"] = round(prob, 3)
        else:
            raise ValueError("unknown class id.")
        return result
