# Simple Jieba

✂️ 用 [100](simjb/token.py) 行实现简单版本的 [jieba](https://github.com/fxsjy/jieba) 分词。

## 使用方法

### 安装

```bash
pip install simjb

# 或者
git clone https://github.com/Ailln/simple-jieba.git
cd simple-jieba
python setup.py install
```

### 使用

```python
import simjb

result = simjb.cut("为中华之崛起而读书！")
print(result)
# ['为', '中华', '之', '崛起', '而', '读书', '！']
```

## 性能对比

由于该简单版本代码只实现了 jieba 分词的核心功能，可以预期的结果是：**分词正确率下降，分词速度上升。**

我使用了 [bakeoff2005](http://sighan.cs.uchicago.edu/bakeoff2005/) 的数据集中的 `Peking University` 训练集和 `Microsoft Research` 训练集进行性能对比，得到的结果如下：

| Peking University(pku) | 正确率（正确词数/所有词数） | 速度（所有词数/花费时间） |
| :--------------------: | :-------------------------: | :-----------------------: |
|         jieba          | 78.54% (871705/1109949)     |   119k (1109949/9.36s)    |
|         simjb          | **80.26%** (890836/1109949)   | **140k** (1109949/7.94s)  |


| Microsoft Research(msr) | 正确率（正确词数/所有词数）  | 速度（所有词数/花费时间） |
| :----------------: | :--------------------------: | :-----------------------: |
|       jieba        |   80.60% (1908851/2368422)   |   130k (2368422/18.22s)   |
|       simjb        | **81.47%** (1929606/2368422) | **177k** (2368422/13.36s) |

然鹅，这两份不同数据集的结果都有些诡异！居然在分词正确率上有小幅度提升，在分词速度上有 **30%** 左右的提升！

我最初从 jieba 的源码中整理出这部分的核心代码，仅仅是希望后人想要学习时，有一份简明易懂的学习资料。从上文的结果来看，这个简单版本似乎是可用的！
（欢迎大家可以做更多的测试来打脸，哈哈哈）

具体的测试方法见[这里](./test/README.md)。

## 源码解析

![](./simjb/src/simple-jieba_flow_v1_20191016-0347.png)

### 1 根据正则规则切分出区块

```python
import re

class Tokenizer(object):
    def __init__(self):
        self.re_cn = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&._%-]+)", re.U)

    def cut(self, sentence):
        block_list = self.re_cn.split(sentence)
        cut_result_list = []
        for block in block_list:
            # 跳过空的 block
            if not block:
                continue
            if self.re_cn.match(block):
                cut_result_list.extend(self.cut_util(block))
            else:
                cut_result_list.append(block)
        return cut_result_list
```

首先将输入的句子进行正则规则切分，其中标点符号会被独立的切分开来，最后得到了一个包含不同区块的列表，等待进一步的切分。

下方是一个例子：

```
# 切分前
快看，是武汉市长江大桥！
# 切分后
["快看", "，", "是武汉市长江大桥", "！"]
```

我们将其中可以正则匹配到的区块（`快看`和`是武汉市长江大桥`）进行处理，进入下一步。

### 2 根据词典生成有向无环图

在这一步我们需要将输入的区块进行切分，构建出一个有向无环图，求出最大概率路径就可以得到区块的最优切分。

构建有向无环图时，我们需要先准备一个带有词频的巨大词典，类似于这样：

```
AT&T 3 nz
B超 3 n
c# 3 nz
C# 3 nz
c++ 3 nz
...
```

每一行有三个值，分别为：`词 词频 词性`。

我们使用的词典来自于 jieba 分词，据说是统计了 98 年人民日报语料和一些小说的分词结果所得。

这样的词典在读取后还不能直接用，我们需要对词典进行预处理，得到一个只包含词和词频的字典。

这个字典指 python 的 dict，就是下面这种：

```
{
    "AT&T": 3,
    "A": 0,
    "AT": 0,
    "AT&": 0,
    "B超": 3,
    "B": 0,
    ...
}
```

不知道你有没有注意到，除了直接添加词和词频，我们还添加每个词的前缀和前缀的词频。

前缀的意思是指，比如我们有个词叫`长江大桥`，那么它前缀就是`长`，`长江`，`长江大`。

添加它为了在下文中匹配词语的时候可以匹配到长词，如果没有前缀，那么`长江大桥`就只能被匹配成`长江`和`大桥`。

前缀的词频是哪里来的呢？我们先判断前缀是否在原来的词典中，如果它在，就不用重复添加了，如果它不在，就把词频设置为 0。

下面的代码描述了详细的构建词频字典的过程。

```python
def _get_freq_dict(self):
    stream = resource_stream(*self.dict_path)
    freq_dict = {}
    freq_total = 0
    for line in stream.readlines():
        word, freq = line.decode("utf-8").split(" ")[:2]
        freq = int(freq)
        freq_dict[word] = freq
        freq_total += freq
        for word_index in range(len(word)):
            word_frag = word[:word_index + 1]
            if word_frag not in freq_dict:
                freq_dict[word_frag] = 0
    return freq_dict, freq_total
```

现在我们要来构建有向无环图了，[有向无环图](https://baike.baidu.com/item/%E6%9C%89%E5%90%91%E6%97%A0%E7%8E%AF%E5%9B%BE)的英文是`Directed Acyclic Graphs`，我们在代码中使用了首字母缩写 `dag` 表示。

下面是构建有向无环图的代码：

```python
def _get_dag(self, sentence):
    dag = {}
    sen_len = len(sentence)
    for i in range(sen_len):
        temp_list = []
        j = i
        frag = sentence[i]
        while j < sen_len and frag in self.freq_dict:
            if self.freq_dict[frag]:
                temp_list.append(j)
            j += 1
            frag = sentence[i:j + 1]
        if not temp_list:
            temp_list.append(i)
        dag[i] = temp_list
    return dag
```

从头遍历所有可能的词（上文中的前缀的作用就在这里），如果它在词频字典中就记录下来，最后构成了一个有向无环图。

有向无环图的存储形式是一个字典，每个元素存储的是以当前字开始可能形成的词语，举例如下：

```
# 快看
{0: [0], 1: [1]}
# 是武汉市长江大桥
{0: [0], 1: [1, 2, 3], 2: [2], 3: [3, 4], 4: [4, 5, 7], 5: [5], 6: [6, 7], 7: [7]}
```

我们来看第二行第五个元素`4: [4, 5, 7]`，它表示的是`（4, 4) (4, 5), (4, 7)`，即 `长 长江 长江大桥`。

### 3 使用动态规划求解最大概率路径

有了区块的有向无环图之后，我们就要想办法求解出最大概率路径了。

使用动态规划反向递推出基于词频的最大切分组合，具体的公式和详细过程参考文末给出资料。代码如下：

```python
def _calc_dag_with_dp(self, sentence):
    dag = self._get_dag(sentence)
    sen_len = len(sentence)
    route = {sen_len: (0, 0)}
    # 取 log 防止数值下溢
    log_total = log(self.freq_total)
    for sen_index in reversed(range(sen_len)):
        freq_list = []
        for word_index in dag[sen_index]:
            word_freq = self.freq_dict.get(sentence[sen_index:word_index + 1])
            # 解决 log(0) 无定义问题, 则取 log(1)=0
            freq_index = (log(word_freq or 1) - log_total + route[word_index + 1][0], word_index)
            freq_list.append(freq_index)
        route[sen_index] = max(freq_list)
    return route
```

这里还使用了一个 trick，使用 log 进行计算来防止 python 数值下溢。

最大切分组合的结果如下：

```
# 是武汉市长江大桥
{8: (0, 0), 7: (-8.863849339256593, 7), 6: (-9.813518371579148, 7), 5: (-19.011818225013663, 5), 4: (-9.653648934289546, 7), 3: (-16.96504852719957, 3), 2: (-25.780438328041008, 2), 1: (-17.531432139245716, 3), 0: (-21.85438660163864, 0)}
```

### 4. 合并所有区块切分结果

得到区块的切分后，还需要处理一些细节，比如英语单词，应该将连续英文字母作为一个整体的英文单词切分。

```python
def cut_util(self, sentence):
    word_index = 0
    word_buf = ""
    result = []
    route = self._calc_dag_with_dp(sentence)
    while word_index < len(sentence):
        word_index_end = route[word_index][1] + 1
        word = sentence[word_index:word_index_end]
        # 匹配出英文
        if self.re_en.match(word) and len(word) == 1:
            word_buf += word
            word_index = word_index_end
        else:
            if word_buf:
                result.append(word_buf)
                word_buf = ""
            else:
                result.append(word)
                word_index = word_index_end
    # 纯英文
    if word_buf:
        result.append(word_buf)
    return result
```

最后把所有结果汇总，分词就完成了！

```
# 输入
快看，是武汉市长江大桥！
# 输出
["快", "看", "，", "是", "武汉市", "长江大桥", "！"]
```

jieba 分词本身要比这个更复杂，除了上文用到的技术，它还使用了 HMM 对未登陆词进行了处理，感兴趣的可以去阅读源码。

## 许可证

[![](https://award.dovolopor.com?lt=License&rt=MIT&rbc=green)](./LICENSE)

## 参考资料

- [jieba源码解析（一）：分词之前](https://www.cnblogs.com/aloiswei/p/11507763.html)
- [jieba源码解析（二）：jieba.cut](https://www.cnblogs.com/aloiswei/p/11567616.html)
- [中文分词工具探析（二）：Jieba](https://www.cnblogs.com/en-heng/p/6234006.html)
- [结巴分词2--基于前缀词典及动态规划实现分词](https://www.cnblogs.com/zhbzz2007/p/6084196.html)
- [不用Trie，减少内存加快速度；优化代码细节](https://github.com/fxsjy/jieba/pull/187)
- [中文分词相关资料](https://github.com/Ailln/nlp-roadmap#1-%E5%88%86%E8%AF%8D-word-segmentation)
- [如何从模板创建仓库？](https://help.github.com/cn/articles/creating-a-repository-from-a-template)
- [如何发布自己的包到 pypi ？](https://www.v2ai.cn/python/2018/07/30/PY-1.html)
