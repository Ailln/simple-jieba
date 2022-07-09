import re
import math
from typing import Dict, List, Tuple
from time import perf_counter
from pkg_resources import resource_stream


class Tokenizer(object):
    def __init__(self) -> None:
        self.dict_path = ["simjb", "src/dict.txt"]
        self.normal_ptn = re.compile(r"([\u4E00-\u9FD5a-zA-Z\d+#&._%-]+)", re.U)
        self.en_ptn = re.compile(r"[a-zA-Z\d]", re.U)
        self.freq_dict = {}
        self.freq_total = 0

        self.__init_freq_dict()

    def cut(self, sentence: str) -> list:
        if type(sentence) != str:
            raise TypeError("sentence must be str!")

        # 以非标点符号分割句子
        text_blocks = self.normal_ptn.split(sentence)
        cut_result = []
        for index, block in enumerate(text_blocks):
            if len(block) > 0:
                if index % 2 == 0:
                    cut_result.append(block)
                else:
                    cut_result.extend(self.__cut_util(block))
        return cut_result

    def add_word(self, word: str, freq: int = 1000) -> None:
        self.freq_total += freq
        self.freq_dict[word] = freq

        # 为了让 dag 能够正常生成，需要将 word 的前缀字符串也加入到 freq_dict 中
        self.__add_prefix_word_to_dict(word)

    def del_word(self, word: str) -> None:
        self.freq_total -= self.freq_dict[word]
        self.freq_dict[word] = 0

    def __cut_util(self, sentence: str) -> list:
        route = self.__calc_route_with_dp(sentence)
        result = []
        word_buf = ""
        word_index = 0
        while word_index < len(sentence):
            word_index_end = route[word_index][0] + 1
            word = sentence[word_index:word_index_end]
            # 匹配出英文
            if self.en_ptn.match(word) and len(word) == 1:
                word_buf += word
                word_index = word_index_end
            else:
                if word_buf:
                    result.append(word_buf)
                    word_buf = ""
                else:
                    result.append(word)
                    word_index = word_index_end
        if word_buf:
            result.append(word_buf)
        return result

    def __calc_route_with_dp(self, sentence: str) -> Dict[int, Tuple[int, int]]:
        dag = self.__build_dag(sentence)
        sen_len = len(sentence)
        route = {sen_len: (0, 0)}
        # 取 log 防止数值下溢；取 log(1)=0 解决 log(0) 无定义问题
        log_total = math.log(self.freq_total or 1)
        for sen_index in reversed(range(sen_len)):
            freq_score = {}
            for word_index in dag[sen_index]:
                word_freq = self.freq_dict.get(sentence[sen_index:word_index + 1])
                freq_score[word_index] = math.log(word_freq or 1) - log_total + route[word_index+1][1]
            route[sen_index] = max(freq_score.items(), key=lambda x: x[1])
        return route

    def __build_dag(self, sentence: str) -> Dict[int, List[int]]:
        dag = {}
        sen_len = len(sentence)
        for i in range(sen_len):
            word_index_list = []
            j = i
            fragment = sentence[i]
            while j < sen_len and fragment in self.freq_dict.keys():
                if self.freq_dict[fragment] > 0:
                    word_index_list.append(j)
                j += 1
                fragment = sentence[i:j+1]
            if not word_index_list:
                word_index_list.append(i)
            dag[i] = word_index_list
        return dag

    def __init_freq_dict(self) -> None:
        start_time = perf_counter()
        with resource_stream(*self.dict_path) as stream:
            for line in stream.readlines():
                word, freq, _ = line.decode("utf-8").split(" ")
                self.freq_dict[word] = int(freq)
                self.freq_total += int(freq)
                self.__add_prefix_word_to_dict(word)
        end_time = perf_counter()
        print(f"[simjb] load freq_dict cost: {end_time - start_time:.2f}s")

    def __add_prefix_word_to_dict(self, word: str) -> None:
        for word_index in range(len(word)-1):
            word_frag = word[:word_index + 1]
            if word_frag not in self.freq_dict.keys():
                self.freq_dict[word_frag] = 0
