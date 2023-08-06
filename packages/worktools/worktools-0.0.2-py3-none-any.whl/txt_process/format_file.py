# -*- coding: UTF-8 -*-
"""
@Project ：MyTools 
@File    ：format_file.py
@IDE     ：PyCharm 
@Author  ：Cheng Xiaozhao
@Date    ：2021/1/12 下午7:58 
"""

from tqdm import tqdm

from .read_file import get_multi_lines


def format_change(origin_path, save_path,
                  format_lens=3, valid_index=None,
                  check_label=True, label_index=0):
    """
    按照文本的标准格式，对原始文本提取有效元素，重新按照标准排列并保存为新文本文件

    :param origin_path: 源文件路径. txt
    :param save_path: 格式化的保存文件路径. txt
    :param format_lens: 每行数据按照空格分割后的标准语句数量. 默认为3句 (text_a, text_b, label)
    :param valid_index: 待提取的有效元素在分割后源数据中的索引序列 (0, 1, 2)
    :param check_label: bool. 是否需要校验label元素为数字格式
    :param label_index: label元素在提取后的列表中的索引位置
    :return: None
    """
    data_lines, lines_len = get_multi_lines(origin_path, return_lens=True)

    list_processed = []
    for i in tqdm(range(lines_len)):
        spline = data_lines[i].strip().split()

        # 判断源格式是否正常，单句内部含有空格会造成分割数量超过预期值，或是元素缺省也会引发异常，该句则剔除
        if len(spline) != format_lens:
            continue

        new_line = []
        for ind in range(format_lens):
            valid_data = spline[valid_index[ind]]
            new_line.append(valid_data)

        # 核验label项是否为数字
        if check_label:
            if not new_line[label_index].isdigital():
                continue

        # 以多个空格分隔提取出的有效元素，形成格式化后的标准行
        format_line = "   ".join(new_line)

        list_processed.append(format_line)
        list_processed.append('\n')

    with open(save_path, 'w') as save_file:
        save_file.writelines(list_processed)
