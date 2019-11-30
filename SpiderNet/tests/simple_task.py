# encoding: utf-8
'''
@author: libingchen
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: nicolas_bch@163.com
@software: garner
@file: simple_task.py
@time: 2019-11-19 10:48
@desc:
'''
import requests, os


base_url = 'http://172.17.6.88:6792/roadmap/?qt=tile&x={x}&y={y}&styles=pl&scaler=2&z={z}'

url_params = [
    {"x": "1~3", "y": "0~1", "z": 4},
    {"x": "5~6", "y": "1~2", "z": 5},
    {"x": "11~12", "y": "2~3", "z": 6},
    {"x": "23~24", "y": "6~7", "z": 7},
    {"x": "47~49", "y": "13~14", "z": 8},
    {"x": "96~97", "y": "26~27", "z": 9},
    {"x": "193~195", "y": "53~54", "z": 10},
    {"x": "387~390", "y": "107~109", "z": 11},
    {"x": "774~780", "y": "214~219", "z": 12},
    {"x": "1548~1560", "y": "428~438", "z": 13},
    {"x": "3096~3120", "y": "856~876", "z": 14}
]

filename = './png_file'

if not os.path.exists(filename):
    os.makedirs(filename)
for params in url_params:
    x_list = params.get('x').split('~')
    y_list = params.get('y').split('~')
    z = params.get('z')
    for x in range(int(x_list[0]), int(x_list[1])+1, 1):
        for y in range(int(y_list[0]), int(y_list[1])+1, 1):
            # x, y, z = 1, 0, 3
            url = base_url.format(x=x, y=y, z=z)
            png_name = '/{y}.png'.format(y=y)
            write_file_name = filename+'/{z}'.format(z=z)+'/{x}'.format(x=x)
            if not os.path.exists(write_file_name):
                os.makedirs(write_file_name)
            with open(write_file_name+png_name, 'wb') as fw:
                fw.write(requests.get(url=url).content)
            # break
        # break
    # break
