# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import os
from codecs import open

from pysenti import tokenizer
from pysenti.compat import strdecode
from pysenti.utils import split_sentence


pwd_path = os.path.abspath(os.path.dirname(__file__))

# 情感词典，包括积极词典、消极词典
sentiment_dict_path = os.path.join(pwd_path, 'data/sentiment_dict.txt')
# 连词词典
conjunction_dict_path = os.path.join(pwd_path, 'data/conjunction_dict.txt')
# 副词词典
adverb_dict_path = os.path.join(pwd_path, 'data/adverb_dict.txt')
# 否定词典
denial_dict_path = os.path.join(pwd_path, 'data/denial_dict.txt')


class RuleClassifier(object):
    def __init__(self):
        self.name = "rule_classifier"
        self.sentiment_dict = {}
        self.conjunction_dict = {}
        self.adverb_dict = {}
        self.denial_dict = {}
        self.user_sentiment_dict = {}
        self.inited = False

    def init(self, sentiment_dict_path=sentiment_dict_path):
        # 加载情感词典词典
        self.sentiment_dict = self._get_dict(sentiment_dict_path)
        self.conjunction_dict = self._get_dict(conjunction_dict_path)  # 连词
        self.adverb_dict = self._get_dict(adverb_dict_path)  # 副词
        self.denial_dict = self._get_dict(denial_dict_path)
        self.inited = True

    def load_user_sentiment_dict(self, path):
        if not self.inited:
            self.init()
        self.user_sentiment_dict = self._get_dict(path)
        self.sentiment_dict.update(self.user_sentiment_dict)

    def classify(self, text):
        if not self.inited:
            self.init()
        # 情感分析整体数据结构
        result = {"score": 0}
        text = strdecode(text)
        # 分句
        clauses = split_sentence(text)
        # 对每分句进行情感分析
        for i in range(len(clauses)):
            # 情感分析子句的数据结构
            sub_clause = self._analyse_clause(clauses[i])

            # 将子句分析的数据结果添加到整体数据结构中
            result["sub_clause" + str(i)] = sub_clause
            result["score"] += sub_clause["score"]

        return result

    def _analyse_clause(self, clause):
        sub_clause = {"score": 0, "sentiment": [], "conjunction": []}
        seg_result = tokenizer.segment(clause, pos=False)

        # 逐个分析分词
        for word in seg_result:
            # 判断是否是连词
            r = self._is_word_conjunction(word)
            if r:
                sub_clause["conjunction"].append(r)

            # 判断是否是情感词
            r = self._is_word_sentiment(word, seg_result)
            if r:
                sub_clause["sentiment"].append(r)
                sub_clause["score"] += r["score"]

        # 综合连词的情感值
        for a_conjunction in sub_clause["conjunction"]:
            sub_clause["score"] *= a_conjunction["value"]

        return sub_clause

    def _is_word_conjunction(self, the_word):
        r = {}
        if the_word in self.conjunction_dict:
            r = {"key": the_word, "value": self.conjunction_dict[the_word]}
        return r

    def _is_word_sentiment(self, the_word, seg_result, index=-1):
        r = {}
        # 判断分词是否在情感词典内
        if the_word in self.sentiment_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            r = self._emotional_word_analysis(the_word, self.sentiment_dict[the_word], seg_result, index)
        # 不在情感词典内，则返回空
        return r

    def _emotional_word_analysis(self, core_word, value, segments, index):
        # 在情感词典内，则构建一个以情感词为中心的字典数据结构
        orientation = {"key": core_word, "adverb": [], "denial": [], "value": value}
        orientation_score = value

        # 在三个前视窗内，判断是否有否定词、副词
        view_window = index - 1
        if view_window > -1:  # 无越界
            # 判断前一个词是否是情感词
            if segments[view_window] in self.sentiment_dict:
                orientation["score"] = orientation_score
                return orientation
            # 判断是否是副词
            if segments[view_window] in self.adverb_dict:
                # 构建副词字典数据结构
                adverb = {"key": segments[view_window], "sentiment": 1,
                          "value": self.adverb_dict[segments[view_window]]}
                orientation["adverb"].append(adverb)
                orientation_score *= self.adverb_dict[segments[view_window]]
            # 判断是否是否定词
            elif segments[view_window] in self.denial_dict:
                # 构建否定词字典数据结构
                denial = {"key": segments[view_window], "sentiment": 1,
                          "value": self.denial_dict[segments[view_window]]}
                orientation["denial"].append(denial)
                orientation_score *= -1
        view_window = index - 2
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.sentiment_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {"key": segments[view_window], "sentiment": 2,
                          "value": self.adverb_dict[segments[view_window]]}
                orientation_score *= self.adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.denial_dict:
                denial = {"key": segments[view_window], "sentiment": 2,
                          "value": self.denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0:
                    # 是，则引入调节阈值，0.3
                    orientation_score *= 0.3
        view_window = index - 3
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.sentiment_dict:
                orientation["score"] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {"key": segments[view_window], "sentiment": 3,
                          "value": self.adverb_dict[segments[view_window]]}
                orientation_score *= self.adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.denial_dict:
                denial = {"key": segments[view_window], "sentiment": 3,
                          "value": self.denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0 and len(orientation["denial"]) == 0:
                    orientation_score *= 0.3
        # 添加情感分析值
        orientation["score"] = orientation_score
        # 返回的数据结构
        return orientation

    @staticmethod
    def _get_dict(path, encoding="utf-8"):
        """
        情感词典的构建
        :param path:
        :param encoding:
        :return:
        """
        sentiment_dict = {}
        with open(path, 'r', encoding=encoding) as f:
            c = 0
            for line in f:
                parts = line.strip().split()
                c += 1
                if len(parts) == 2:
                    sentiment_dict[parts[0]] = float(parts[1])
                else:
                    print("error", c, line)
        return sentiment_dict


if __name__ == '__main__':
    d = RuleClassifier()

    a_sentence = ['剁椒鸡蛋好难吃。绝对没人受得了',
                  '土豆丝很好吃', '土豆丝很难吃',
                  '这笔钱是个天文数字',
                  '我一会儿出去玩了，你吃啥？给你带,然而你不知道']
    for i in a_sentence:
        r = d.classify(i)
        print(i, r)
