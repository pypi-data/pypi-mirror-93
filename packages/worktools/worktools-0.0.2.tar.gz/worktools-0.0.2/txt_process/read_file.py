# -*- coding: utf-8 -*-
"""
@Project ：MyTools
@File    ：read_file.py
@IDE     ：PyCharm
@Author  ：Cheng Xiaozhao
@Date    ：
@Desc    ：读取txt文档，获取相关信息     若需修改此函数，应通过对应测试用例的自动检验才可以
"""


def get_multi_lines(txt_path, return_lines=True, return_lens=False):
    """
    获取TXT文档的多行内容，及对应的行数

    :param txt_path: txt文档路径
    :param return_lines: 是否返回多行数据
    :param return_lens: 是否返回总行数
    :return: 多行内容和行数，或二者之一
    """
    try:
        with open(txt_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error：文件路径异常，请检查该路径文件是否存在，或是否为TXT格式")

    else:
        if return_lines and return_lens:
            line_lens = len(lines)

            return lines, line_lens

        elif return_lines:
            return lines

        elif return_lens:
            line_lens = len(lines)

            return line_lens

        else:
            print("Warning：兄弟，至少要返回一种结果吧，不然你图啥呢？")
            return -1


if __name__ == '__main__':
    file_path = "test_data/map_dict.txt"

    lens = get_multi_lines(file_path)
    print(lens)

"""
cmd
PYTHONPATH=. python txt_process/read_file.py
"""
