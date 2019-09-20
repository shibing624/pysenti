# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 配置切词器
"""
import logging

import jieba
from jieba import posseg

jieba.default_logger.setLevel(logging.ERROR)


def segment(sentence, cut_type='word', pos=False):
    """
    切词
    :param sentence:
    :param cut_type: 'word' use jieba.lcut; 'char' use list(sentence)
    :param pos: enable POS
    :return: list
    """
    if pos:
        if cut_type == 'word':
            word_pos_seq = posseg.lcut(sentence)
            word_seq, pos_seq = [], []
            for w, p in word_pos_seq:
                word_seq.append(w)
                pos_seq.append(p)
            return word_seq, pos_seq
        elif cut_type == 'char':
            word_seq = list(sentence)
            pos_seq = []
            for w in word_seq:
                w_p = posseg.lcut(w)
                pos_seq.append(w_p[0].flag)
            return word_seq, pos_seq
    else:
        if cut_type == 'word':
            return jieba.lcut(sentence)
        elif cut_type == 'char':
            return list(sentence)
