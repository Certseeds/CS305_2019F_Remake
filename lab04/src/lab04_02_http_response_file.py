#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 16:38:58 
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
from lab04.src.lab04_02_http_response import *


class http_response_file(http_response):
    def __init__(self, file_path: str, method: str, file_type: str):
        super().__init__()
        self.file_type: str = file_type
        self.method: str = method
        self.msg: bytes = get_file(file_path)
        if self.file_type is None:
            self.file_type = 'application/octet-stream'
            self.set_headers('Accept-Ranges', 'bytes')
        self.set_headers('Content-Type', self.file_type)
        self.set_headers('Content-Length', str(len(self.msg)))

    def get_response(self) -> bytes:
        if self.method == 'HEAD':
            return get_string(self.head_normal).encode()
        elif self.method == 'GET':
            return get_string(self.head_normal).encode() + self.msg
