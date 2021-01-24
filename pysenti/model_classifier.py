# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

from pysenti.bayes import Bayes
from pysenti.compat import strdecode
from pysenti.tokenizer import segment
from pysenti.utils import filter_stop


class ModelClassifier(object):
    def __init__(self, model_path):
        self.classifier = Bayes()
        self.model_path = model_path
        self.inited = False

    def save(self):
        self.classifier.save(self.model_path)

    def load(self):
        self.classifier.load(self.model_path)
        self.inited = True

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

    def classify(self, text):
        """
        sentiment classification text
        :param text: text, str
        :return:    "positive_prob": 0.0,
                    "negative_prob": 0.0
                    dict
        """
        if not self.inited:
            self.load()
        result = {"positive_prob": 0.0, "negative_prob": 0.0}
        text = strdecode(text)
        ret, prob = self.classifier.classify(self.handle(text))
        if ret == 'pos':
            result["positive_prob"] = round(prob, 3)
            result["negative_prob"] = round(1 - prob, 3)
        elif ret == 'neg':
            result["positive_prob"] = round(1 - prob, 3)
            result["negative_prob"] = round(prob, 3)
        else:
            raise ValueError("unknown class id.")
        return result


if __name__ == '__main__':
    model = ModelClassifier('./data/sentiment_model.pkl')
    a_sentence = ['剁椒鸡蛋好难吃。绝对没人受得了',
                  '土豆丝很好吃', '土豆丝很难吃',
                  '这笔钱是个天文数字',
                  '我一会儿出去玩了，你吃啥？给你带']
    for i in a_sentence:
        r = model.classify(i)
        print(i, r)
