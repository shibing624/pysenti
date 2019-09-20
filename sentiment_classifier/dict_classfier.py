# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

import re
from collections import defaultdict
from jieba import posseg
from sentiment_classifier.tokenizer import segment
from sentiment_classifier import config

class DictClassifier(object):
    def __init__(self):
        # 加载情感词典词典
        self.__phrase_dict = self.__get_phrase_dict(config.phrase_dict_path)
        self.__positive_dict = self.__get_dict(config.positive_dict_path)
        self.__negative_dict = self.__get_dict(config.negative_dict_path)
        self.__conjunction_dict = self.__get_dict(config.conjunction_dict_path)
        self.__punctuation_dict = self.__get_dict(config.punctuation_dict_path)
        self.__adverb_dict = self.__get_dict(config.adverb_dict_path)
        self.__denial_dict = self.__get_dict(config.denial_dict_path)

    def classify(self, sentence):
        return self.analyse_sentence(sentence)

    def analyse_sentence(self, sentence, runout_filepath=None, print_show=False):
        # 情感分析整体数据结构
        comment_analysis = {"score": 0}

        # 将评论分句
        the_clauses = self.__divide_sentence_into_clauses(sentence + "%")

        # 对每分句进行情感分析
        for i in range(len(the_clauses)):
            # 情感分析子句的数据结构
            sub_clause = self.__analyse_clause(the_clauses[i].replace("。", "."), runout_filepath, print_show)

            # 将子句分析的数据结果添加到整体数据结构中
            comment_analysis["su-clause" + str(i)] = sub_clause
            comment_analysis['score'] += sub_clause['score']

        if runout_filepath is not None:
            # 将整句写进运行输出文件，以便复查
            self.__write_runout_file(runout_filepath, "\n" + sentence + '\n')
            # 将每个评论的每个分句的分析结果写进运行输出文件，以便复查
            self.__output_analysis(comment_analysis, runout_filepath)
            # 将每个评论的的整体分析结果写进运行输出文件，以便复查
            self.__write_runout_file(runout_filepath, str(comment_analysis) + "\n\n\n\n")
        if print_show:
            print("\n" + sentence)
            self.__output_analysis(comment_analysis)
            print(comment_analysis, end="\n\n\n")

        if comment_analysis["score"] > 0:
            return 1
        else:
            return 0

    def __analyse_clause(self, the_clause, runout_filepath, print_show):
        sub_clause = {"score": 0, "positive": [], "negative": [], "conjunction": [], "punctuation": [], "pattern": []}
        seg_result = posseg.lcut(the_clause)

        # 将分句及分词结果写进运行输出文件，以便复查
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, the_clause + '\n')
            self.__write_runout_file(runout_filepath, str(seg_result) + '\n')
        if print_show:
            print(the_clause)
            print(seg_result)

        # 判断句式：如果……就好了
        judgement = self.__is_clause_pattern2(the_clause)
        if judgement != "":
            sub_clause["pattern"].append(judgement)
            sub_clause["score"] -= judgement["value"]
            return sub_clause

        # 判断句式：是…不是…
        judgement = self.__is_clause_pattern1(the_clause)
        if judgement != "":
            sub_clause["pattern"].append(judgement)
            sub_clause["score"] -= judgement["value"]

        # 判断句式：短语
        judgement = self.__is_clause_pattern3(the_clause, seg_result)
        if judgement != "":
            sub_clause["score"] += judgement["score"]
            if judgement["score"] >= 0:
                sub_clause["positive"].append(judgement)
            elif judgement["score"] < 0:
                sub_clause["negative"].append(judgement)
            match_result = judgement["key"].split(":")[-1]
            i = 0
            while i < len(seg_result):
                if seg_result[i].word in match_result:
                    if i + 1 == len(seg_result) or seg_result[i + 1].word in match_result:
                        del (seg_result[i])
                        continue
                i += 1

        # 逐个分析分词
        for i in range(len(seg_result)):
            mark, result = self.__analyse_word(seg_result[i].word, seg_result, i)
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

    @staticmethod
    def __is_clause_pattern2(the_clause):
        # re_pattern = re.compile(r".*(如果|要是|希望).+就[\u4e00-\u9fa5]+(好|完美)了")
        re_pattern = re.compile(r".*(如果|要是|希望).+就[\u4e00-\u9fa5]*(好|完美)了")
        match = re_pattern.match(the_clause)
        if match is not None:
            pattern = {"key": "如果…就好了", "value": 1.0}
            return pattern
        return ""

    def __is_clause_pattern3(self, the_clause, seg_result):
        for a_phrase in self.__phrase_dict:
            keys = a_phrase.keys()
            to_compile = a_phrase["key"].replace("……", "[\u4e00-\u9fa5]*")

            if "start" in keys:
                to_compile = to_compile.replace("*", "{" + a_phrase["start"] + "," + a_phrase["end"] + "}")
            if "head" in keys:
                to_compile = a_phrase["head"] + to_compile

            match = re.compile(to_compile).search(the_clause)
            if match is not None:
                can_continue = True
                pos = [flag for word, flag in posseg.cut(match.group())]
                if "between_tag" in keys:
                    if a_phrase["between_tag"] not in pos and len(pos) > 2:
                        can_continue = False

                if can_continue:
                    for i in range(len(seg_result)):
                        if seg_result[i].word in match.group():
                            try:
                                if seg_result[i + 1].word in match.group():
                                    return self.__emotional_word_analysis(
                                        a_phrase["key"] + ":" + match.group(), a_phrase["value"],
                                        [x for x, y in seg_result], i)
                            except IndexError:
                                return self.__emotional_word_analysis(
                                    a_phrase["key"] + ":" + match.group(), a_phrase["value"],
                                    [x for x, y in seg_result], i)
        return ""

    def __analyse_word(self, the_word, seg_result=None, index=-1):
        # 判断是否是连词
        judgement = self.__is_word_conjunction(the_word)
        if judgement != "":
            return 1, judgement

        # 判断是否是标点符号
        judgement = self.__is_word_punctuation(the_word)
        if judgement != "":
            return 2, judgement

        # 判断是否是正向情感词
        judgement = self.__is_word_positive(the_word, seg_result, index)
        if judgement != "":
            return 3, judgement

        # 判断是否是负向情感词
        judgement = self.__is_word_negative(the_word, seg_result, index)
        if judgement != "":
            return 4, judgement

        return 0, ""

    @staticmethod
    def __is_clause_pattern1(the_clause):
        re_pattern = re.compile(r".*(要|选)的.+(送|给).*")
        match = re_pattern.match(the_clause)
        if match is not None:
            pattern = {"key": "要的是…给的是…", "value": 1}
            return pattern
        return ""

    def __is_word_conjunction(self, the_word):
        if the_word in self.__conjunction_dict:
            conjunction = {"key": the_word, "value": self.__conjunction_dict[the_word]}
            return conjunction
        return ""

    def __is_word_punctuation(self, the_word):
        if the_word in self.__punctuation_dict:
            punctuation = {"key": the_word, "value": self.__punctuation_dict[the_word]}
            return punctuation
        return ""

    def __is_word_positive(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.__positive_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self.__emotional_word_analysis(the_word, self.__positive_dict[the_word],
                                                  [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def __is_word_negative(self, the_word, seg_result, index):
        # 判断分词是否在情感词典内
        if the_word in self.__negative_dict:
            # 在情感词典内，则构建一个以情感词为中心的字典数据结构
            return self.__emotional_word_analysis(the_word, self.__negative_dict[the_word],
                                                  [x for x, y in seg_result], index)
        # 不在情感词典内，则返回空
        return ""

    def __emotional_word_analysis(self, core_word, value, segments, index):
        # 在情感词典内，则构建一个以情感词为中心的字典数据结构
        orientation = {"key": core_word, "adverb": [], "denial": [], "value": value}
        orientation_score = orientation["value"]  # my_sentiment_dict[segment]

        # 在三个前视窗内，判断是否有否定词、副词
        view_window = index - 1
        if view_window > -1:  # 无越界
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or \
                            segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            # 判断是否是副词
            if segments[view_window] in self.__adverb_dict:
                # 构建副词字典数据结构
                adverb = {"key": segments[view_window], "position": 1,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation["adverb"].append(adverb)
                orientation_score *= self.__adverb_dict[segments[view_window]]
            # 判断是否是否定词
            elif segments[view_window] in self.__denial_dict:
                # 构建否定词字典数据结构
                denial = {"key": segments[view_window], "position": 1,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].append(denial)
                orientation_score *= -1
        view_window = index - 2
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or \
                            segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 2,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 2,
                          "value": self.__denial_dict[segments[view_window]]}
                orientation["denial"].insert(0, denial)
                orientation_score *= -1
                # 判断是否是“不是很好”的结构（区别于“很不好”）
                if len(orientation["adverb"]) > 0:
                    # 是，则引入调节阈值，0.3
                    orientation_score *= 0.3
        view_window = index - 3
        if view_window > -1:
            # 判断前一个词是否是情感词
            if segments[view_window] in self.__negative_dict or segments[view_window] in self.__positive_dict:
                orientation['score'] = orientation_score
                return orientation
            if segments[view_window] in self.__adverb_dict:
                adverb = {"key": segments[view_window], "position": 3,
                          "value": self.__adverb_dict[segments[view_window]]}
                orientation_score *= self.__adverb_dict[segments[view_window]]
                orientation["adverb"].insert(0, adverb)
            elif segments[view_window] in self.__denial_dict:
                denial = {"key": segments[view_window], "position": 3,
                          "value": self.__denial_dict[segments[view_window]]}
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
    def __output_analysis(self, comment_analysis, runout_filepath=None):
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
            # if clause["pattern"] is not None:
            #     output += "pattern:" + clause["pattern"]["key"] + " "
            output += "\n"
        if runout_filepath is not None:
            self.__write_runout_file(runout_filepath, output)
        else:
            print(output)

    def __divide_sentence_into_clauses(self, the_sentence):
        the_clauses = self.__split_sentence(the_sentence)

        the_clauses[-1] = the_clauses[-1][:-1]
        return the_clauses

    @staticmethod
    def __split_sentence(sentence):
        pattern = re.compile("[，。%、！!？?,；～~.… ]+")

        split_clauses = pattern.split(sentence.strip())
        punctuations = pattern.findall(sentence.strip())
        try:
            split_clauses.remove("")
        except ValueError:
            pass
        punctuations.append("")

        clauses = [''.join(x) for x in zip(split_clauses, punctuations)]

        return clauses

    def __get_phrase_dict(self,path):
        sentiment_dict = []
        pattern = re.compile(r"\s+")
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                a_phrase = {}
                result = pattern.split(line.strip())
                if len(result) >= 2:
                    a_phrase["key"] = result[0]
                    a_phrase["value"] = float(result[1])
                    for i, a_split in enumerate(result):
                        if i < 2:
                            continue
                        else:
                            a, b = a_split.split(":")
                            a_phrase[a] = b
                    sentiment_dict.append(a_phrase)

        return sentiment_dict

    # 情感词典的构建
    @staticmethod
    def __get_dict(path, encoding="utf-8"):
        sentiment_dict = {}
        pattern = re.compile(r"\s+")
        with open(path, encoding=encoding) as f:
            for line in f:
                result = pattern.split(line.strip())
                if len(result) == 2:
                    sentiment_dict[result[0]] = float(result[1])
        return sentiment_dict

    @staticmethod
    def __write_runout_file(path, info, encoding="utf-8"):
        with open(path, "a", encoding=encoding) as f:
            f.write("%s" % info)

if __name__ == '__main__':
    d = DictClassifier()
    a_sentence = ['剁椒鸡蛋好难吃','土豆丝很好吃']
    for i in a_sentence:
        result = d.analyse_sentence(i)
        print(i, result)