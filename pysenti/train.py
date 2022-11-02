# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import os
from codecs import open

from pysenti.model_classifier import ModelClassifier


def train(neg_file, pos_file, model_path):
    neg = open(neg_file, 'r', 'utf-8').readlines()
    pos = open(pos_file, 'r', 'utf-8').readlines()
    neg_docs = []
    pos_docs = []
    for line in neg:
        neg_docs.append(line.rstrip("\r\n"))
    for line in pos:
        pos_docs.append(line.rstrip("\r\n"))
    global classifier
    classifier = ModelClassifier(model_path)
    classifier.train(neg_docs, pos_docs)


def save():
    classifier.save()


def classify(sent):
    return classifier.classify(sent)


if __name__ == '__main__':
    pwd_path = os.path.abspath(os.path.dirname(__file__))
    default_sentiment_model_path = os.path.join(pwd_path, 'data/sentiment_model.pkl')

    train('data/neg_sentences.txt', 'data/pos_sentences.txt', default_sentiment_model_path)
    save()
    txt = "苹果是一家伟大的公司"
    print(txt, ' prob: ', classify(txt))
