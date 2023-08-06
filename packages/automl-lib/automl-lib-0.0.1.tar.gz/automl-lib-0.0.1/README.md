
# 使用方法，对外提供两个方法build_framework，export_saved_model
'''
# -*- coding: utf-8 -*-
# @Author : Zip
# @Time   : 2020/12/18|12:53
# @Moto   : Knowledge comes from decomposition
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import warnings
from lib.estimator import build_framework
from lib.export import export_saved_model
import argparse

warnings.filterwarnings('ignore')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file", default="conf/job_sort_with_fm_with_two_feature.yaml")
    args = parser.parse_args()

    build_framework(args.config_file)
    # export_saved_model(args.config_file)


if __name__ == '__main__':
    main()


'''