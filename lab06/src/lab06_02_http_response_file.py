#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 16:38:58 
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
from lab06.src.lab06_02_http_response import *


class http_response_file(http_response):
    def __init__(self, file_path: str, method: str, file_type: str):
        super().__init__()
        self.file_type: str = file_type
        self.method: str = method
        # self.msg: bytes = self.get_file(file_path)
        if self.file_type is None:
            self.file_type = 'application/octet-stream'
        self.set_headers('Content-Type', self.file_type)
        if file_type[0:4] != "text":
            self.delete_charset('; charset=utf-8\r\n')
            self.set_headers('Content-Type', file_type + '\r\n')
        # self.set_headers('Content-Length', str(len(self.msg)))
        self.set_headers('Accept-Ranges', 'bytes')

    def get_response(self) -> bytes:
        if self.method == 'HEAD':
            return get_string(self.head_normal).encode()
        elif self.method == 'GET':
            return get_string(self.head_normal).encode() + self.msg

    def get_file(self, file_name: str, begin: int, length: int, use_range: bool):
        try:
            file = open(file_name, mode='rb')
        except FileNotFoundError:
            return b'Not Found'
        will_return: bytes = file.read()
        file.close()
        if length == -1:
            length = len(will_return) - begin
        if use_range:
            if length != 0 and not (begin >= len(will_return) or begin + length > len(will_return)):
                self.head_normal[0] = "HTTP/1.0 {} {}\r\n".format(206, state_code_msg[206])
            elif (begin >= len(will_return) or begin + length > len(will_return)):
                self.head_normal[0] = "HTTP/1.0 {} {}\r\n".format(416, state_code_msg[416])
                begin = 0
                length = len(will_return)
        else:
            begin = 0
            length = len(will_return)
        self.set_headers('Content-Range', "bytes {}-{}/{}".format(begin, begin + length - 1, len(will_return)))
        self.set_headers('Content-Length', str(len(will_return[begin:begin + length])))
        print("length is {}".format(length))
        self.msg = will_return[begin:begin + length]
