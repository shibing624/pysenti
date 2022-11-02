# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import os
import pickle
import re
from codecs import open


def load_set(path):
    words = set()
    with open(path, 'r', 'utf-8') as f:
        for line in f:
            words.add(line.strip())
    return words


re_zh = re.compile('([\u4E00-\u9FA5]+)')


def filter_stop(words, stopwords):
    return list(filter(lambda x: x not in stopwords, words))


def load_pkl(pkl_path):
    """
    加载词典文件
    :param pkl_path:
    :return:
    """
    with open(pkl_path, 'rb') as f:
        result = pickle.load(f)
    return result


def dump_pkl(vocab, pkl_path, overwrite=True):
    """
    存储文件
    :param pkl_path:
    :param overwrite:
    :return:
    """
    if pkl_path and os.path.exists(pkl_path) and not overwrite:
        return
    if pkl_path:
        with open(pkl_path, 'wb') as f:
            pickle.dump(vocab, f, protocol=0)
        print("save %s ok." % pkl_path)
    else:
        raise IOError("no file: %s" % pkl_path)


def split_sentence(sentence):
    pattern = re.compile(u"[，。%、！!？?,；～~.… ]+")
    clauses = [i for i in pattern.split(sentence.strip()) if i]
    return clauses


if __name__ == '__main__':
    sent = "nihao,我是警察，你站起来。我要问你话！好不。"
    k = split_sentence(sent)
    print(k)
