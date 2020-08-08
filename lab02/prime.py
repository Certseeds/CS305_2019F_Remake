#!/usr/bin/env python3
# coding=utf-8
'''
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2019-12-23 10:33:34
@LastEditors: nanoseeds
@LastEditTime: 2020-06-20 10:19:27
'''
""" CS305_Network
    Copyright (C) 2020  nanoseeds

    CS305_Network is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    CS305_Network is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import List


def find_prime(start: int, end: int) -> List[int]:
    prime_array: List[int] = []
    for i in range(start, end + 1):
        if judge_is_prime(i):
            prime_array.append(i)
    return prime_array


def judge_is_prime(number: int) -> bool:
    if number == 2:
        return True
    max_value: int = (int)((number) ** (1 / 2)) + 1
    for i in range(2, max_value + 1):
        if number % i == 0:
            return False
    return True


def main():
    print(find_prime(2, 100))


if __name__ == '__main__':
    main()
