from functools import reduce, partial

import jmespath


class JsReader:
    def __init__(self, value: any):
        self.jsview = value


class JsPath:
    def __init__(self, path: str):
        self.js_path = path
        self._init = False
        self._value = None
        self._proc = list()

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

    def filter(self, jmespath_query: str):
        self._proc.append(partial(jmespath.search, jmespath_query))

    def __get__(self, obj: JsReader, objtype=None):
        if self._init:
            return self._value
        self._value = reduce(lambda memo, item: item(memo), self._proc, jmespath.search(self.js_path, obj.jsview))
        return self._value
