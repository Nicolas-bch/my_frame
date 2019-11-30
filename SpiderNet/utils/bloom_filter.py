# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: bloom_filter.py
@time: 2019-11-26 17:30
@desc:
'''

from public.redis_api import connection


class HashMap:
    def __init__(self, m, seed):
        self.m = m
        self.seed = seed

    def hash(self, value):
        """
        Hash Algorithm
        :param value: value
        :return: hash value
        """
        ret = 0
        for i in range(len(value)):
            ret += self.seed*ret + ord(value[i])
        return (self.m - 1) & ret


class BloomFilter:
    def __init__(self, key='bloom_filter', bit=30, hash_number=6):
        """
        Initialize BloomFilter
        :param server: redis server
        :param key: bloom_filter key
        :param bit: m = 2 ^ bit
        :param hash_number: the number of hash function
        """
        # default to 1<<30 = 10,7374,1824 = 2^30 = 128MB, max filter 2^30/hash_number = 1,7895,6970 fingerprints
        self.m = 1<<bit
        self.seeds = range(hash_number)
        self.server = connection()
        self.key = 'bloom_filter'+'_'+key
        self.maps = [HashMap(self.m, seed) for seed in self.seeds]
        pass

    def is_exist(self, value):
        """
        if value exist
        :param value:
        :return:
        """
        if not value:
            return False
        exist = True
        for map in self.maps:
            offset = map.hash(value)
            exist = exist & self.server.getbit(self.key, offset)
        return exist

    def insert(self, value):
        """
        add value to bloom
        :param value:
        :return:
        """
        for f in self.maps:
            offset = f.hash(value)
            self.server.setbit(self.key, offset, 1)

    def count(self):
        return self.server.bitcount(self.key)//6