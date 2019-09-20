# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description:
"""


def process(text):
    """
    调用情感倾向分析
    :param text:
    :return:
    """
    result = {"sentiment": 1,
              "confidence": 0.0,
              "positive_prob": 0.0,
              "negative_prob": 0.0}
    try:
        # r = client.sentimentClassify(text)
        print(text)
    except UnicodeEncodeError as e:
        print("error", e)
    except Exception as es:
        print("error", es)
    return result


if __name__ == '__main__':
    texts = ["苹果是一家伟大的公司", "我刚去吃饭了", "你到底在干嘛呀", "我以前是个小偷，现在是个警察了",
             "再也不敢吃紫菜了",
             "我正在刘鑫描述凶案事发过程江歌母亲在日请愿判凶手死刑的主页，朋友们快来看看吧",
             "王者荣耀游戏风靡校园。据了解，在上海和国内不少城市的中小学校，玩王者荣耀的学生比例不低。有小学生称，"
             "班里有同学为了玩游戏，凌晨3点起床，一直打到6点，再去上学。专家表示，中小学生痴迷游戏并非好事，父母要适当引导和干预。"]
    for i in texts:
        r = process(i)
        print(i, r)
