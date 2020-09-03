#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 23:32:36
@LastEditors: nanoseeds
"""
""" CS305_2019F_Remake 
    Copyright (C) 2020  nanoseeds

    CS305_2019F_Remake is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    CS305_2019F_Remake is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from lab05.src.lab05_03_helper_functions import *


class dns_querys(object):
    def __init__(self, bin: bytes):
        """
        其中Header部分的长度是固定的,但是其他的长度都是不定的,需要对二进制串进行处理,再从中得出信息
        Part A:
        形式为  {Number (几个八位数组表示的字符) } * n +00,表示xxx.xxx.xxx.xxx + 一个终结提示符
        Part B,Part C:两个八位数组代码 * 2,一个代表查询类型,另一个表示查询的类
        所以,首要问题是从中判断Part A,然后part b,c就顺理成章了,这里面直接寻找终结提示符:"00"就可
        :param bin: 传入的byte流,将被拆成小块
        """
        data: List[int] = list(bin)
        self.id: List[int] = data[0:2]
        self.header: List[int] = data[0:12]
        # data[10:12] = [0, 0]
        domain_finish = get_ques_domain_end(data, 12)
        self.ques_name: List[int] = data[12:domain_finish]
        self.ques_type: List[int] = data[domain_finish:domain_finish + 2]
        self.ques_class: List[int] = data[domain_finish + 2:domain_finish + 4]
        self.re_question: bytes = bytes(data[0:domain_finish + 4])
        self.Answers: List[int] = data[domain_finish + 4:]

    def get_querys_header_question(self) -> List[int]:
        return list_poly(self.header, self.get_querys_question())

    def get_querys_question(self) -> List[int]:
        return list_poly(self.ques_name, self.ques_type, self.ques_class)

    def get_querys_all(self) -> bytes:
        return bytes(list_poly(self.header, self.get_querys_question(), self.Answers))


if __name__ == '__main__':
    for posi in range(1, 20):
        print((posi // 8) * 8 + ((posi % 8) != 0) * 8)
    header1: dns_querys = dns_querys(
        b'\xcf\x9b\x01\x20\x00\x01\x00\x00\x00\x00\x00\x01\x03www\x05baidu\x03com\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\t\xd0l?\x1dY\x0b\x93')
    x: int = 1
