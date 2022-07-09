from .token import Tokenizer

t = Tokenizer()
cut = t.cut
add_word = t.add_word
del_word = t.del_word

__version__ = "0.2.0"

__all__ = [
    "__version__",
    "cut",
    "add_word",
    "del_word"
]
