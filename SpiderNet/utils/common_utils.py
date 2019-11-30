# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: common_utils.py
@time: 2019-11-12 16:47
@desc:
'''

import hashlib


def md(obj):
    md5 = hashlib.md5()
    md5.update(str(obj).encode('utf-8'))
    return md5.hexdigest()

