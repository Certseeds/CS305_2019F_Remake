#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-21 11:54:28 
@LastEditors  : nanoseeds
"""
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
from typing import Tuple, List


def get_string(*args: Tuple[List[str]]) -> str:
    will_return: str = ""
    for i in args:
        will_return += get_string_in(i)
    return will_return


def get_string_in(array: List[str]) -> str:
    will_return: str = ""
    for i in array:
        will_return += i
    return will_return


def get_file(file_name: str) -> bytes:
    try:
        file = open(file_name, mode='rb')
    except FileNotFoundError:
        return b'Not Found'
    will_return: bytes = file.read()
    file.close()
    return will_return
