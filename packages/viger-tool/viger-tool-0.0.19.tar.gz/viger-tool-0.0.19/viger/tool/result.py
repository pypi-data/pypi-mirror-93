#!/usr/bin/env python

import io
import sys
import time
from .json import json

# Format Result
class Result():
    """
    函数执行结果格式化
    OK: 是否成功(True|False)
    line: 代码哪一行输入
    data: 输出的结果
    time: 从初始化到设值的时间
    """
    OK = True
    line = ''
    data = ''
    time = 0

    def __init__(self):
        self.set_dict()
        self._time = time.time()

    def __str__(self):
        if isinstance(self.data, str):
            return self.data
        elif isinstance(self.data, list):
            return json.dumps(self.data, indent=2, ensure_ascii=False)
        elif isinstance(self.data, dict):
            return json.dumps(self.data, indent=2, ensure_ascii=False)
        else:
            return str(self.data)

    def __repr__(self):
        return self.__str__()

    def set(self, data, OK=True):
        filename = sys._getframe(1).f_code.co_filename
        line = sys._getframe(1).f_lineno

        self.OK = OK
        self.line = '{}(line:{})'.format(filename, line)
        self.data = data
        self.time = '%0.3f'%(time.time() - self._time)
        self.set_dict()

    def set_dict(self):
        self.dict = {
            'OK': self.OK,
            'line': self.line,
            'data': self.data,
            'time': self.time,
        }

    def __getitem__(self, key):
        return self.dict[key]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __len__(self):
        return len(self.dict)

    def __contains__(self, key):
        return key in self.dict
