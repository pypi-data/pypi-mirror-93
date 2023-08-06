# -*- coding: utf-8 -*-
"""
@Project ：MyTools
@File    ：split_file.py
@IDE     ：PyCharm
@Author  ：Cheng Xiaozhao
@Date    ：
@Desc    ：拆分txt文件
"""

import os
from tqdm import tqdm

from txt_process import read_file


def split2single(total_txt_path, single_txt_dir, start_name_index=0):
    """
    将多行的大文件，按行拆分成多个单独的小文件

    :param total_txt_path: 大文件路径
    :param single_txt_dir: 拆分后的多个文件所在目录
    :param start_name_index: 拆分后的文件命名起始值，后续依次递增
    :return: None
    """
    os.makedirs(single_txt_dir, exist_ok=True)

    lines, lines_len = read_file.get_multi_lines(total_txt_path, return_lens=True)

    for i in tqdm(range(lines_len)):
        data = lines[i].strip('\n')

        anno_name = str(start_name_index) + '.txt'
        anno_path = os.path.join(single_txt_dir, anno_name)
        with open(anno_path, 'w') as anno_txt:
            anno_txt.writelines(data)

        start_name_index = start_name_index + 1


if __name__ == '__main__':
    file_path = "test_data/map_dict.txt"
    files_dir = 'test_data/maps'

    split2single(file_path, files_dir)

"""
cmd
PYTHONPATH=. python txt_process/split_file.py
"""
