#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : conf
# @Time         : 2021/1/31 10:20 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


class TrainConf(BaseConfig):
    epoch = 10
    batch_size = 128


def train(**kwargs):
    logger.info("开始训练")
    time.sleep(3)


def run(**kwargs):
    logger.info(f"kwargs: {kwargs}")
    c = TrainConf.parse_obj(kwargs)
    train(**c.dict())


conf_cli = fire.Fire(run)

