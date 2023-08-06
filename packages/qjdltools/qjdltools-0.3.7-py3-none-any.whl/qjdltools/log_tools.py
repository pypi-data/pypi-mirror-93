# -*- coding:utf-8 -*-
'''
Tools for log.

Version 1.0  2020-12-08 15:26:09 by QiJi
'''
import time


def time_str():
    return time.strftime("%H:%M:%S", time.localtime())
