import unittest

from .token import Tokenizer


class TokenizerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.input_data = {
           "为中华之崛起而读书": ['为', '中华', '之', '崛起', '而', '读书']
        }

        self.t = Tokenizer()

    def test_an2cn(self) -> None:
        for item in self.input_data.keys():
            print(self.t.cut(item))
            self.assertEqual(self.t.cut(item), self.input_data[item])


if __name__ == '__main__':
    unittest.main()
