
[![PyPI version](https://badge.fury.io/py/pysenti.svg)](https://badge.fury.io/py/pysenti)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/shibing624/pysenti/LICENSE)
![Language](https://img.shields.io/badge/Language-Python-blue.svg)


# pysenti

Chinese Sentiment Classification Tool for Python. 中文情感极性分析工具。

**pysenti**基于规则词典的情感极性分析，扩展性强，可作为调研用的基准方法。

## Question
文本情感极性（倾向）分析咋做？

## Solution
### 规则的解决思路
1. 中文情感极性分析，文本切分为段落，再切词，通过情感词标识出各个词语的情感极性，包括积极、中立、消极。
2. 结合句子结构（包括连词、否定词、副词、标点等）给各情感词语的情感极性赋予权重，然后加权求和得到文本的情感极性得分。
3. 优点：泛化性好，规则可扩展性强，所有领域通用。
4. 缺点：规则词典收集困难，专家系统的权重设定有局限，单一领域准确率相比模型方法低。

### 模型的解决思路
1. 常见的[NLP文本分类模型](https://github.com/shibing624/text-classifier)均可，包括经典文本分类模型（LR、SVM、Xgboost等）和深度文本分类模型（TextCNN、Bi-LSTM、BERT等）。
2. 优点：单一领域准召率高。
3. 缺点：不通用，有标注数据的样本收集困难，扩展性弱。

## Feature
### 规则
* [情感词典](https://github.com/shibing624/pysenti/tree/master/pysenti/data)整合了`知网情感词典`、`清华大学李军情感词典`、[BosonNLP情感词典](https://bosonnlp.com/dev/resource)、`否定词词典`。

### 模型
* bayes 文本分类模型
* [样本数据](https://github.com/shibing624/pysenti/tree/master/pysenti/data)来自商品评论数据，分为积极、消极两类。

## Demo

https://www.mulanai.com/product/sentiment_classify/

## Install
* 全自动安装：pip3 install pysenti
* 半自动安装：
```
git clone https://github.com/shibing624/pysenti.git
cd pysenti
python3 setup.py install
```

## Usage
### 规则方法
```
import pysenti

texts = ["苹果是一家伟大的公司",
         "土豆丝很好吃",
         "土豆丝很难吃"]
for i in texts:
    r = pysenti.classify(i)
    print(i, r['score'], r)

```

output:
```
苹果是一家伟大的公司 3.4346924811096997 {'score': 3.4346924811096997, 'sub_clause0': {'score': 3.4346924811096997, 'sentiment': [{'key': '苹果', 'adverb': [], 'denial': [], 'value': 1.37846341627, 'score': 1.37846341627}, {'key': '是', 'adverb': [], 'denial': [], 'value': -0.252600480826, 'score': -0.252600480826}, {'key': '一家', 'adverb': [], 'denial': [], 'value': 1.48470161748, 'score': 1.48470161748}, {'key': '伟大', 'adverb': [], 'denial': [], 'value': 1.14925252286, 'score': 1.14925252286}, {'key': '的', 'adverb': [], 'denial': [], 'value': 0.0353323193687, 'score': 0.0353323193687}, {'key': '公司', 'adverb': [], 'denial': [], 'value': -0.360456914043, 'score': -0.360456914043}], 'conjunction': []}}
土豆丝很好吃 2.294311221077 {'score': 2.294311221077, 'sub_clause0': {'score': 2.294311221077, 'sentiment': [{'key': '土豆丝', 'adverb': [], 'denial': [], 'value': 0.294892711165, 'score': 0.294892711165}, {'key': '很', 'adverb': [], 'denial': [], 'value': 0.530242664632, 'score': 0.530242664632}, {'key': '好吃', 'adverb': [], 'denial': [], 'value': 1.46917584528, 'score': 1.46917584528}], 'conjunction': []}}
土豆丝很难吃 -2.381874203563 {'score': -2.381874203563, 'sub_clause0': {'score': -2.381874203563, 'sentiment': [{'key': '土豆丝', 'adverb': [], 'denial': [], 'value': 0.294892711165, 'score': 0.294892711165}, {'key': '很', 'adverb': [], 'denial': [], 'value': 0.530242664632, 'score': 0.530242664632}, {'key': '难吃', 'adverb': [], 'denial': [], 'value': -3.20700957936, 'score': -3.20700957936}], 'conjunction': []}}
```
> score: 正值是积极情感；负值是消极情感。

### 模型方法


```
from pysenti import model_classifier

texts = ["苹果是一家伟大的公司",
         "土豆丝很好吃",
         "土豆丝很难吃"]
for i in texts:
    result = model_classifier.classify(i)
    print(i, result)

```

output：
```
苹果是一家伟大的公司 {'positive_prob': 0.682, 'negative_prob': 0.318}
土豆丝很好吃 {'positive_prob': 0.601, 'negative_prob': 0.399}
土豆丝很难吃 {'positive_prob': 0.283, 'negative_prob': 0.717}

```

### 延迟加载机制

pysenti 采用延迟加载，`import pysenti` 和 `from pysenti import rule_classifier` 不会立即触发词典的加载，一旦有必要才开始加载词典。如果你想手工初始 pysenti，也可以手动初始化。
```
import pysenti
pysenti.rule_classifier.init()  # 手动初始化（可选）
```

有了延迟加载机制后，你可以改变主词典的路径:
```
pysenti.rule_classifier.init('data/sentiment_dict.txt')
```

### 命令行

使用示例： python -m pysenti news.txt > news_result.txt

命令行选项（翻译）：
```
使用: python -m pysenti [options] filename

命令行界面

固定参数:
  filename              输入文件

可选参数:
  -h, --help            显示此帮助信息并退出
  -d DICT, --dict DICT  使用 DICT 代替默认词典
  -u USER_DICT, --user-dict USER_DICT
                        使用 USER_DICT 作为附加词典，与默认词典或自定义词典配合使用
  -a, --output-all      输出句子及词级别情感分析详细信息
  -V, --version         显示版本信息并退出

如果没有指定文件名，则使用标准输入。
```


`--help`选项输出：
```
$> python -m pysenti --help

usage: python3 -m pysenti [options] filename

pysenti command line interface.

positional arguments:
  filename              input file

optional arguments:
  -h, --help            show this help message and exit
  -d DICT, --dict DICT  use DICT as dictionary
  -u USER_DICT, --user-dict USER_DICT
                        use USER_DICT together with the default dictionary or
                        DICT (if specified)
  -a, --output-all      output text sentiment score and word sentiment info
  -V, --version         show program's version number and exit

If no filename specified, use STDIN instead.
```

## Reference

- snownlp
- SentimentPolarityAnalysis
