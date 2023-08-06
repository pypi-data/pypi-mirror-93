# -*- coding: UTF-8 -*-
"""
@Project ：MyTools 
@File    ：debug.py
@IDE     ：PyCharm 
@Author  ：Cheng Xiaozhao
@Date    ：2021/1/12 下午8:28 
"""

from .format_file import format_change


if __name__ == '__main__':
    file_path = "test_data/map_dict.txt"
    files_dir = 'test_data/maps'

    format_change()

"""
cmd
PYTHONPATH=. python txt_process/split_file.py
"""
