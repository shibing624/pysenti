# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import re

from sentiment_classifier import config
from sentiment_classifier.tokenizer import segment
from sentiment_classifier.utils import split_sentence


class DictClassifier(object):
    def __init__(self):
        # 加载情感词典词典
        self.positive_dict = self._get_dict(config.positive_dict_path)
        self.negative_dict = self._get_dict(config.negative_dict_path)
        self.conjunction_dict = self._get_dict(config.conjunction_dict_path)  # 连词
        self.punctuation_dict = self._get_dict(config.punctuation_dict_path)
        self.adverb_dict = self._get_dict(config.adverb_dict_path)  # 副词
        self.denial_dict = self._get_dict(config.denial_dict_path)

    def classify(self, sentence, print_show=True):
        # 情感分析整体数据结构
        comment_analysis = {"score": 0}
        # 分句
        clauses = split_sentence(sentence)
        # 对每分句进行情感分析
        for i in range(len(clauses)):
            # 情感分析子句的数据结构
            sub_clause = self._analyse_clause(clauses[i], print_show)

            # 将子句分析的数据结果添加到整体数据结构中
            comment_analysis["su-clause" + str(i)] = sub_clause
            comment_analysis['score'] += sub_clause['score']

        if print_show:
            print("\n" + sentence)
            self._output_analysis(comment_analysis)
            print(comment_analysis, end="\n\n\n")

        return comment_analysis["score"]

    def _analyse_clause(self, clause, print_show):
        sub_clause = {"score": 0, "positive": [], "negative": [], "conjunction": [], "punctuation": [], "pattern": []}
        seg_result = segment(clause, pos=True)

        # 将分句及分词结果写进运行输出文件，以便复查
        if print_show:
            print(clause)
            print(seg_result)

        # 逐个分析分词
        for i in range(len(seg_result)):
            mark, result = self._analyse_word(seg_result[i].word, seg_result, i)
            if mark == 0:
                continue
            elif mark == 1:
                sub_clause["conjunction"].append(result)
            elif mark == 2:
                sub_clause["punctuation"].append(result)
            elif mark == 3:
                sub_clause["positive"].append(result)
                sub_clause["score"] += result["score"]
            elif mark == 4:
                sub_clause["negative"].append(result)
                sub_clause["score"] -= result["score"]

        # 综合连词的情感值
        for a_conjunction in sub_clause["conjunction"]:
            sub_clause["score"] *= a_conjunction["value"]

        # 综合标点符号的情感值
        for a_punctuation in sub_clause["punctuation"]:
            sub_clause["score"] *= a_punctuation["value"]

        return sub_clause


    def _analyse_word(self, the_word, seg_result=None, index=-1):
        # 判断是否是连词
        judgement = self._is_word_conjunction(the_word)
        if judgement != "":
            return 1, judgement

        # 判断是否是标点符号
        judgement = self._is_word_punctuation(the_word)
        if judgement != "":
            return 2, judgement

        # 判断是否是正向情感词
        judgement = self._is_word_positive(the_word, seg_result, index)
        if judgement != "":
            return 3, judgement

        # 判断是否是负向情感词
        judgement = self._is_word_negative(the_word, seg_result, index)
        if judgement != "":
            return 4, judgement

        return 0, ""

    def _is_word_conjunction(self, the_word):
        if the_word in self.conjunction_dict:
            conjunction = {"key": the_word, "value": self.conjunction_dict[the_word]}
            return conjunction
        return ""

    def _is_word_punctuation(self, the_word):
        if the_word in self.punctuation_dict:
            punctuation = {"key": the_word, "value": self.punctuation_dict[the_word]}
            return punctuation
        return ""

    def _is_word_positive(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.positive_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self._emotional_word_analysis(the_word, self.positive_dict[the_word],
                                                 [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def _is_word_negative(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.negative_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self._emotional_word_analysis(the_word, self.negative_dict[the_word],
                                                 [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def _emotional_word_analysis(self, core_word, value, segments, index):
        # 在情感词典内，则构建一个以情感词为中心的字典数据结构
        orientation = {"key": core_word, "adverb": [], "denial": [], "value": value}
        orientation_score = orientation["value"]  # my_sentiment_dict[segment]

        # 在三个前视窗内，判断是否有否定词、副词
        view_window = index - 1
        if view_window > -1:  # 无越界
            # 判断前一个词是否是情感词
            if segments[view_window] in self.negative_dict or \
                            segments[view_window] in self.positive_dict:
                orientation['score'] = orientation_score
                return orientation
            # 判断是否是副词
            if segments[view_window] in self.adverb_dict:
                # 构建副词字典数据结构
                adverb = {"key": segments[view_window], "position": 1,
                          "value": self.adverb_dict[segments[view_window]]}
                orientation["adverb"].append(adverb)
                orientation_score *= self.adverb_dict[segments[view_window]]
            # 判断是否是否定词
            elif segments[view_window] in self.denial_dict:
                # 构建否定词字典数据结构
                denial = {"key": segments[view_window], "position": 1,
                          "value": self.denial_dict[segments[view_window]]}
                orientation["denial"].append(denial)
                orientation_score *= -1
        view_window = index - 2
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.negative_dict or \
                            segments[view_window] in self.positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {"key": segments[view_window], "position": 2,
                          "value": self.adverb_dict[segments[view_window]]}
                orientation_score *= self.adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.denial_dict:
                denial = {"key": segments[view_window], "position": 2,
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
            if segments[view_window] in self.negative_dict or segments[view_window] in self.positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.adverb_dict:
                adverb = {"key": segments[view_window], "position": 3,
                          "value": self.adverb_dict[segments[view_window]]}
                orientation_score *= self.adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.denial_dict:
                denial = {"key": segments[view_window], "position": 3,
                          "value": self.denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0 and len(orientation["denial"]) == 0:
                    orientation_score *= 0.3
        # 添加情感分析值。
        orientation['score'] = orientation_score
        # 返回的数据结构
        return orientation

    # 输出comment_analysis分析的数据结构结果
    def _output_analysis(self, comment_analysis):
        output = "Score:" + str(comment_analysis["score"]) + "\n"

        for i in range(len(comment_analysis) - 1):
            output += "Sub-clause" + str(i) + ": "
            clause = comment_analysis["su-clause" + str(i)]
            if len(clause["conjunction"]) > 0:
                output += "conjunction:"
                for punctuation in clause["conjunction"]:
                    output += punctuation["key"] + " "
            if len(clause["positive"]) > 0:
                output += "positive:"
                for positive in clause["positive"]:
                    if len(positive["denial"]) > 0:
                        for denial in positive["denial"]:
                            output += denial["key"] + str(denial["position"]) + "-"
                    if len(positive["adverb"]) > 0:
                        for adverb in positive["adverb"]:
                            output += adverb["key"] + str(adverb["position"]) + "-"
                    output += positive["key"] + " "
            if len(clause["negative"]) > 0:
                output += "negative:"
                for negative in clause["negative"]:
                    if len(negative["denial"]) > 0:
                        for denial in negative["denial"]:
                            output += denial["key"] + str(denial["position"]) + "-"
                    if len(negative["adverb"]) > 0:
                        for adverb in negative["adverb"]:
                            output += adverb["key"] + str(adverb["position"]) + "-"
                    output += negative["key"] + " "
            if len(clause["punctuation"]) > 0:
                output += "punctuation:"
                for punctuation in clause["punctuation"]:
                    output += punctuation["key"] + " "
            if len(clause["pattern"]) > 0:
                output += "pattern:"
                for pattern in clause["pattern"]:
                    output += pattern["key"] + " "
            output += "\n"
        print(output)

    @staticmethod
    def _get_dict(path, encoding="utf-8"):
        """
        情感词典的构建
        :param path:
        :param encoding:
        :return:
        """
        sentiment_dict = {}
        with open(path, encoding=encoding) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    sentiment_dict[parts[0]] = float(parts[1])
                elif len(parts) == 1:
                    sentiment_dict[parts[0]] = 1.0
                else:
                    print('error: ', line)
        return sentiment_dict


if __name__ == '__main__':
    d = DictClassifier()
    a_sentence = ['剁椒鸡蛋好难吃。居然有人受得了', '土豆丝很好吃', '土豆丝很难吃']
    for i in a_sentence:
        result = d.classify(i)
        print(i, result)
