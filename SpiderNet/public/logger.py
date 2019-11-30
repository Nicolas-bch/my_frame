#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-27 14:36:20
# @Author  : RoryXiang (pingping19901121@gmail.com)
# @Link    : ${link}
# @Version : $Id$

import yaml
import os
import logging.config
path = "./conf/logging.yml"
log_folder = "./log"


def setup_logging():
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    if os.path.exists(path):
        with open(path, "rt") as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


def add_logger_handler(logger, file_name):
    new_ch = logging.FileHandler("./log/" + file_name)
    new_formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - [function:%(funcName)s] - '
        '[line:%(lineno)d] - %(levelname)s: %(message)s')
    new_ch.setFormatter(new_formatter)
    new_ch.setLevel(logging.INFO)
    new_ch.__setattr__("backupCount", 20)
    new_ch.__setattr__("maxBytes", 10485760)
    new_ch.__setattr__("encoding", "utf-8")
    logger.addHandler(new_ch)
