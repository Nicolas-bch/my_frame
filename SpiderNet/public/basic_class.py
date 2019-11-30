#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/11/12 10:37
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ""
# @Version : 1.0

from public.mysql_api import Dbconn
from public.dequeue import Dequeue
from public.mongo_api import get_mongo_db
from conf import settings


class DBClass(object):
    def __init__(self, mysql_info=None, send_queue=None, recv_queue=None):
        self.mongo_db = get_mongo_db()
        self.mysql_db = Dbconn(db_name=mysql_info.db,
                               host=mysql_info.host,
                               passwd=mysql_info.passwd,
                               user=mysql_info.user) if mysql_info else ''
        self.queue_send_name = send_queue
        self.queue_send = Dequeue(queue_name=self.queue_send_name) if self.queue_send_name else ''
        self.queue_recv_name = recv_queue
        self.queue_recv = Dequeue(queue_name=self.queue_recv_name) if self.queue_recv_name else ''

    def send_to_queue(self, task):
        if self.queue_send:
            self.queue_send.send(queue_name=self.queue_send_name, body_info=task.json_dumps_to_str())
        else:
            raise ModuleNotFoundError

    def get_from_queue(self, callback):
        if self.queue_recv:
            self.queue_recv.get(queue_name=self.queue_recv_name, callback=callback)
        else:
            raise ModuleNotFoundError

    def get_mysql_data(self, sql):
        if self.mysql_db:
            data_rows = self.mysql_db.select_by_sql(sql)
            return data_rows
        else:
            raise ModuleNotFoundError

    def get_mongo_data(self, mongo_table, query):
        datas = self.mongo_db[mongo_table].find(query)
        return datas
        pass
