import unittest

from txt_process.read_file import get_multi_lines


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        print("------开始------")
        self.file_path = "test_data/map_dict.txt"

    def tearDown(self) -> None:
        print("------结束------")

    def test_get_lines(self):
        lines_data = get_multi_lines(self.file_path)
        self.assertEqual('0', lines_data[0].split()[0])
        self.assertEqual('1', lines_data[1].split()[0])
        self.assertEqual('[PAD]', lines_data[-1].split()[0])

    def test_get_len(self):
        lines_len = get_multi_lines(self.file_path, return_lines=False, return_lens=True)

        self.assertEqual(lines_len, 4466)


if __name__ == '__main__':
    unittest.main()

"""
command in the root dir of project

PYTHONPATH=. python txt_process/my_unittest/test_read_file.py
"""
