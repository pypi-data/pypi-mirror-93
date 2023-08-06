from functools import reduce, partial

from bs4 import BeautifulSoup


class BsReader(BeautifulSoup):
    pass


class BsPath:
    def __init__(self, css_selector: str, many: bool = False):
        self.css_selector = css_selector
        self.many = many
        self._proc = list()
        self._init = None
        self._value = None

    def map(self, fn):
        def mmap(value):
            return fn(value)

        self._proc.append(mmap)
        return self

    def flatmap(self, fn):
        def mflatmap(value):
            return map(fn, value)

        self._proc.append(mflatmap)
        return self

    def __get__(self, obj: BsReader, objtype=None):
        if self._init:
            return self._value
        value = obj.select_one(self.css_selector) if not self.many else obj.select(self.css_selector)
        self._value = reduce(lambda memo, item: item(memo), self._proc, value)
        return self._value


def as_attr(attr, default, node):
    return node.attrs.get(attr, default)


as_href = partial(as_attr, 'href', '')
