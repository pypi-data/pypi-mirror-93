#! /usr/bin/python3
# -*- coding: utf-8 -*- 
# @File     :mapping.py
# @Time     :2021/1/26
# @Author   :jiawei.li
# @Software :PyCharm
# @Desc     :None

import sklearn.metrics as metrics
import sklearn.linear_model as linear_model
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as model_selection
import sklearn.tree as tree

# MAPPING = {
#     # ------------------------------------------------------- Transorm Component
#     'MinMaxScaler':MinMaxScaler,
#     'QuantileTransformer': QuantileTransformer,
#     'PowerTransformer': PowerTransformer,
#     # ------------------------------------------------------- End Transorm Component
#
#     # ------------------------------------------------------- Training Component
#     'LinearRegression': LinearRegression,
#     'Ridge': Ridge,
#     'RidgeCV': RidgeCV
#     # ------------------------------------------------------- End Training Component
# }

# TODO(jiawei.li@shopee.com): To many module need to load ?
MAPPING_CLASS = [
    metrics,
    linear_model,
    preprocessing,
    model_selection,
    tree,
]

def build_mapping(modules):
    mapping_dict = {}
    for module in modules:
        all = module.__all__
        for item in all:
            mapping_dict[item] = getattr(module, item)
    return mapping_dict

def mapping(func_name, mapping_classes = MAPPING_CLASS):
    mapping_dict = build_mapping(mapping_classes)
    return mapping_dict[func_name]
