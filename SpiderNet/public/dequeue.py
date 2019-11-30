# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: dequeue.py
@time: 2019-11-08 11:09
@desc:
'''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pika
import random

# http://localhost:15672

class Dequeue:
    def __init__(self, host='localhost', queue_name=''):
        hostname = host
        parameters = pika.ConnectionParameters(hostname)
        self.connection = pika.BlockingConnection(parameters)
        # 创建通道
        self.channel = self.connection.channel()
        # durable声明队列持久性，即RabbitMQ重启队列仍旧不丢失（不完全可靠）
        # 对现有队列进行durable声明更改无法生效，只有重新声明一个新的队列才生效
        self.channel.queue_declare(queue=queue_name, durable=True)

    def __del__(self):
        self.connection.close()

    def send(self, queue_name, body_info):
        # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
        # 发送消息到RabbitMQ消息队列里
        self.channel.basic_publish(
            exchange='',  # 指定交换器
            routing_key=queue_name,  # 要绑定的队列
            body=body_info,  # 要发送的消息
            properties=pika.BasicProperties(
                delivery_mode=2,  # 通过delivery_mode=2将队列内的消息持久化
            )
        )

    def callback(cls, ch, method, properties, body):
        # 定义构建回调函数
        print(ch)
        # time.sleep(20)
        print("[x] received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)    # 接收端回复消息给rabbixmq，代表该消息处理已完成

    def get(self, queue_name, callback=None, no_ack=True):
        # 默认情况下，RabbitMQ循环把消息发送给consumer，
        # 通过basic_qos(prefetch_count=1)设置，可以在处理并确认完前一个消息之前，不再接收新信息
        # 即实现“能者多劳”的效果
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue_name,
            self.callback if not callback else callback,
            no_ack,  # 如果为True，rabbitmq会在consumer接收到数据时就删除队列中的消息
        )
        print("[*] waiting for messages. To exit press CTRL+C...")
        self.channel.start_consuming()

    def msg_count(self, queue_name, is_durable=True):
        queue = self.channel.queue_declare(queue=queue_name, durable=True)
        count = queue.method.message_count
        return count
