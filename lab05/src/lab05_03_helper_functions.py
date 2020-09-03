#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 23:43:01
@LastEditors: nanoseeds
@LastEditTime: 2020-06-23 23:29:36
"""
# !/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 23:43:01 
@LastEditors  : nanoseeds
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

from typing import List, Tuple


def trans_bit_toint(int1: int, int2: int, value: int = 8) -> int:
    return (int1 << value) + int2


# just use in trant a int to length_four_ttls
def trans_int_tobit(value: int) -> List[int]:
    will_return: List[int] = []
    for i in range(4):
        will_return.insert(0, value % 256)
        value = value // 256
    return will_return


def list_poly(*args: Tuple[List[int]]) -> List[int]:
    will_return: List[int] = []
    for i in args:
        will_return += i
    return will_return


def get_ques_domain_end(data: List[int], begin: int) -> int:
    # in there, the ques domain's
    posi: int = begin
    while data[posi] != 0:
        if data[posi] == 0xc0:
            return posi + 2
        else:
            posi += (data[posi] + 1)
    # posi -= 12
    # return (posi // 8) * 8 + ((posi % 8) != 0) * 8 + 12
    # name no need to keep 是8的倍数
    return posi + 1


if __name__ == '__main__':
    temp = [3, 11, 11, 11, 5, 11, 22, 33, 44, 55, 6, 12, 23, 34, 45, 56, 78, 0xc0, 16]
    print(get_ques_domain_end(temp, 0))
    print(temp[0:18])
    print(temp[0:19])
