#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-20 12:39:31 
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
keys = ('method', 'path')


class HTTPHeader:

    def __init__(self):
        self.headers = {key: None for key in keys}


def parse_header(self, line):
    fileds = line.split(' ')
    if fileds[0] == 'GET' or fileds[0] == 'POST' or fileds[0] == 'HEAD':
        self.headers['method'] = fileds[0]
        self.headers['path'] = fileds[1]


def get(self, key):
    return self.headers.get(key)

