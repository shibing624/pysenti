# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import os
from pysenti.bayes import Bayes
from pysenti.compat import strdecode
from pysenti.tokenizer import segment
from pysenti.utils import filter_stop, load_set

pwd_path = os.path.abspath(os.path.dirname(__file__))
default_sentiment_model_path = os.path.join(pwd_path, 'data/sentiment_model.pkl')
# 停用词
default_stopwords_path = os.path.join(pwd_path, 'data/stopwords.txt')

class ModelClassifier:
    def __init__(self, model_path=default_sentiment_model_path, stopwords_path=default_stopwords_path):
        self.classifier = Bayes()
        self.model_path = model_path
        self.stopwords = load_set(stopwords_path)
        if model_path:
            self.classifier.load(self.model_path)

    def save(self):
        self.classifier.save(self.model_path)

    def handle(self, doc):
        words = segment(doc)
        words = filter_stop(words, self.stopwords)
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
        result = {"positive_prob": 0.0, "negative_prob": 0.0}
        text = strdecode(text)
        ret, prob = self.classifier.classify(self.handle(text))
        if ret == 'pos':
            result["positive_prob"] = prob
            result["negative_prob"] = 1 - prob
        else:
            result["negative_prob"] = prob
            result["positive_prob"] = 1 - prob
        return result


if __name__ == '__main__':
    model = ModelClassifier()
    a_sentence = ['剁椒鸡蛋好难吃。绝对没人受得了',
                  '土豆丝很好吃', '土豆丝很难吃',
                  '这笔钱是个天文数字',
                  '我一会儿出去玩了，你吃啥？给你带']
    for i in a_sentence:
        r = model.classify(i)
        print(i, r)
