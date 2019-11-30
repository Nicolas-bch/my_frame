# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: mysql_api.py
@time: 2019-11-08 20:44
@desc:
'''
import pymysql
from DBUtils import PersistentDB
import redis
import json


class Pool(PersistentDB.PersistentDB):
    def __enter__(self):
        return self.connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.thread.connection.close()

def clean(fun):
    CLEAR_VALUES=[None]
    def __clean(dbConn,values,*args,**kwargs):
        if isinstance(values,dict):
            keys = [key for key in values.keys() if values[key] in CLEAR_VALUES]
            [values.pop(key) for key in keys]
        return fun(dbConn,values,*args,**kwargs)
    return __clean


class Dbconn:
    """mysql数据库连接池"""
    def __init__(self, db_name=None, table_name=None, host=None, port=3306, passwd=None, user=None):
        self.db_name = db_name
        self.table_name = table_name
        databases = {'host': host, 'user': user, 'passwd': passwd, 'database': db_name,
                     'cursorclass': pymysql.cursors.DictCursor, "charset": "utf8", 'port': port,'autocommit':True}
        self.pool = Pool(creator=pymysql, maxusage=1, closeable=True, **databases)

    def set_table_name(self, table_name):
        self.table_name = table_name


    def select_by_sql(self, sql):
        state = True
        with self.pool as con:
            with con.cursor() as cursor:
                cursor.execute(sql)
                res =cursor.fetchall()
                # cursor.close()
        return (state,res)
    def execute_sql(self, sql):
        state = True
        with self.pool as con:
            with con.cursor() as cursor:
                cursor.execute(sql)
                con.commit()
                cursor.close()
        return state
    @clean
    def insertOrUpdateUniqueIndex(self,values,path=100):
        '''
         :argument values 中需要有唯一索引
          con = DbConn( host='101.236.32.51', port=3306, user='root', passwd='qingyunfei', db_name='crawl',table_name='source_page')
    state,res = con.insertOrUpdateUniqueIndex(
        values=
        [
            {'site_code':'10001','group_code':'2','url':'http://www.baidu.com'},
            {'site_code':'10001','group_code':'2','url':'http://www.baidu.com1'},
            {'site_code':'10001','group_code':'2','url':'http://www.baidu.com2'},

        ])
    print(state,res)
        '''
        state = True
        res = []
        names = list(values[0].keys())
        _values = []
        for value in values:
            _v = []
            for name in names:
                _v.append(str(value.get(name)))
            _values.append(tuple(_v))
        sql = 'insert into {} ({}) values ({}) on DUPLICATE KEY UPDATE {}'.format(self.table_name,', '.join('`{}` '.format(name) for name in names),', '.join('%s' for name in names),', '.join('`{}`=values({})'.format(name,name) for name in names))
        for i in range(len(_values)//path+1):
            with self.pool as con:
                with con.cursor() as cursor:
                    res = cursor.executemany(sql,_values[i*path:(i+1)*path])
                    con.commit()
                    # cursor.close()
        return (state,res)

    def select(self, table_name, values, where_dict):
        state, where = self.genAndSqlWithWhere(where_dict, where_dict.keys())
        if (state == False):
            return (False, 0)
        sql = "SELECT {} FROM `{}` WHERE {}".format(','.join(values), table_name, where)
        with self.pool as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                res = cursor.fetchall()
                # cursor.close()
        return (True, res)
    @clean
    def genAndSqlWithWhere(self, values, where_list):
        # values = pymysql.escape_dict(values,charset='utf-8')
        sql_values = []
        for item in where_list:
            if (item not in values):
                return (False, "")
            v = ''
            sp = "="
            if (isinstance(values[item], str)):
                v = str(pymysql.escape_string(values[item]))
                v = v.strip(" \t\n")
                if v=="?":
                    v = 0
            else:
                v = values[item]
            if " " in item:
                item_list = item.split(" ")
                sp = item_list[1]
                item = item_list[0]
            if (sp == "in"):
                if (isinstance(v, list)) :
                    sql_values.append(" `{}` {} ({})".format(item,sp, ",".join("'{}'".format(x) for x in v)))
                else:
                    sql_values.append(" `{}` {} ('{}')".format(item,sp, v))
                continue
            sql_values.append(" `{}` {} '{}'".format(item,sp, v))
        return (True, " and ".join(sql_values))
    @clean
    def getItemsNameStr(self, dict):
        str = ""
        for item in dict.keys():
            str += '`{}`,'.format(item)
        str = str.rstrip(",")
        return str
    @clean
    def getItemsValueStr(self, dict):
        value = ""
        for item in dict.keys():
            v = ""
            if (isinstance(dict[item], str)):
                v = str(pymysql.escape_string(dict[item]))
                v = v.strip(" \t\n")
                if v == "?":
                    v = 0
            else:
                v = dict[item]
            value += "'{}',".format(v)
        value = value.rstrip(",")
        return value
    @clean
    def insert(self, values):
        # values=pymysql.escape_dict(values,charset='utf-8')
        # print(values)
        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(self.table_name, self.getItemsNameStr(values),
                                                       self.getItemsValueStr(values))
        return self.execute_sql(sql)
    @clean
    def update(self, values, where_list):
            state, where = self.genAndSqlWithWhere(values, where_list)
            if (state == False):
                return (False,0)
            sql = "SELECT {} FROM `{}` WHERE {}".format(','.join(values.keys()),self.table_name, where)
            state,res = self.select_by_sql(sql)
            if (res != None and len(res) > 0):
                state, values_sql = self.genAndSql(values, ",")
                sql = "UPDATE `{}` SET {} WHERE {}".format(self.table_name, values_sql, where)
                self.execute_sql(sql)
                return (True, len(res))
            else:
                return (True, 0)
    @clean
    def genAndSql(self, values, spliter):
        # values = pymysql.escape_dict(values,charset='utf-8')
        sql_values = []
        for item in values.keys():
            v = ''
            sp = "="
            if (isinstance(values[item], str)):
                v = str(pymysql.escape_string(values[item]))
                v = v.strip(" \t\n")
                if v == "?":
                    v = 0
            else:
                v = values[item]

            if v == '':
                print("crawl field {} is '' ".format(item))
            else:
                if " " in item:
                    item_list = item.split(" ")
                    sp = item_list[1]
                    item = item_list[0]
                #需要仔细看下
                sql_values.append(" `{}` {} '{}'".format(item,sp, v))
        return (True, " {} ".format(spliter).join(sql_values))

    @clean
    def updateOrInsert(self, values, where_list):
        state, row_count = self.update(values, where_list)
        if (state == True):
            if (row_count > 0):
                return True
            else:
                return self.insert(values)
        return False