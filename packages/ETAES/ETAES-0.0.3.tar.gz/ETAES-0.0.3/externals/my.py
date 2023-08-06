#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :my.py
# @Time     :2021/2/4
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import pandas as pd

def func(inputs, p):
    inputs['a_mean'] = inputs['a'].mean()
    inputs['b_mean'] = inputs['b'].mean()
    inputs['c_mean'] = inputs['c'].mean()
    return inputs

def func2(inputs, a):
    inputs['a_mean'] = inputs['a'].max()
    inputs['b_mean'] = inputs['b'].max()
    inputs['c_mean'] = inputs['c'].max()
    return inputs