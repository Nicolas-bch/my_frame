# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: models.py
@time: 2019-11-09 10:09
@desc:
'''


class DBConf:
    def __init__(self,host,port=3306,db='test',user='root',passwd=''):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd


if __name__ == '__main__':
    pass