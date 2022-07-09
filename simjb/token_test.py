import unittest

from .token import Tokenizer


class TokenizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.input_data = {
            "武汉市长江大桥": ["武汉市", "长江大桥"],
            "为中华之崛起而读书": ["为", "中华", "之", "崛起", "而", "读书"],
            "成大事者，厚积而薄发！": ["成", "大事", "者", "，", "厚积", "而", "薄", "发", "！"],
            "1飞冲天，2龙戏珠": ["1", "飞", "冲天", "，", "2", "龙", "戏", "珠"],
        }
        self.input_data_with_add_word = [
            {
                "text": "武汉市长江大桥",
                "words": {
                    "大桥": 100000000,
                },
                "result": ["武汉市", "长江", "大桥"]
            },
            {
                "text": "为中华之崛起而读书",
                "words": {
                    "中华之": 100,
                    "崛起而": 100,
                },
                "result": ["为", "中华之", "崛起而", "读书"]
            },
            {
                "text": "成大事者，厚积而薄发！",
                "words": {
                    "薄发": 100,
                },
                "result": ["成", "大事", "者", "，", "厚积", "而", "薄发", "！"]
            },
            {
                "text": "1飞冲天，2龙戏珠",
                "words": {
                    "1飞": 100,
                    "2龙": 10000,
                },
                "result": ["1飞", "冲天", "，", "2龙", "戏", "珠"]
            },
        ]

        self.input_data_with_del_word = [
            {
                "text": "武汉市长江大桥",
                "words": ["长江大桥"],
                "result": ["武汉市", "长江", "大桥"]
            },
            {
                "text": "为中华之崛起而读书",
                "words": ["中华", "崛起"],
                "result": ["为", "中", "华", "之", "崛", "起", "而", "读书"]
            },
            {
                "text": "成大事者，厚积而薄发！",
                "words": ["厚积"],
                "result": ["成", "大事", "者", "，", "厚", "积", "而", "薄", "发", "！"]
            },
            {
                "text": "1飞冲天，2龙戏珠",
                "words": ["冲天"],
                "result": ["1", "飞", "冲", "天", "，", "2", "龙", "戏", "珠"]
            },
        ]

        self.t = Tokenizer()
        self.t_add = Tokenizer()
        self.t_del = Tokenizer()

    def test_cut(self) -> None:
        for item in self.input_data.keys():
            self.assertEqual(self.t.cut(item), self.input_data[item])

        for item in self.input_data_with_add_word:
            for key, value in item["words"].items():
                self.t_add.add_word(key, value)
            self.assertEqual(self.t_add.cut(item["text"]), item["result"])

        for item in self.input_data_with_del_word:
            for word in item["words"]:
                self.t_del.del_word(word)
            self.assertEqual(self.t_del.cut(item["text"]), item["result"])


if __name__ == "__main__":
    unittest.main()
