#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-22 21:42:52 
@LastEditors  : nanoseeds
"""
import time

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
from abc import ABCMeta, abstractmethod
from lab06.src.lab06_02_helper_functions import *

state_code_msg: Mapping[int, str] = {
    206: "Partial Content",
    302: "Found",
    404: "Not Found",
    405: "Method Not Allowed",
    416: "Requested Range Not Satisfiable"
}


class http_response(metaclass=ABCMeta):
    def __init__(self):
        self.head_normal: List[str] = ['HTTP/1.0 200 OK\r\n',
                                       'Connection: close\r\n',
                                       'Cache-Control: no-cache\r\n'
                                       'Server: nanoseeds\r\n',
                                       'Content-Type:text/html',
                                       '; charset=utf-8\r\n',
                                       '\r\n'
                                       ]

    @abstractmethod
    def get_response(self) -> bytes:
        pass

    def set_headers(self, name: str, v: str):
        change_line: str = ('' if (name == 'Content-Type') else '\r\n')
        for index, value in enumerate(self.head_normal):
            if value.count(':') > 0 and value.split(':')[0] == name:
                self.head_normal[index] = name + ': ' + v + change_line
                return
        self.head_normal.insert(-1, "{}{} {}{}".format(name, ":", v, change_line))

    def set_cookie(self, cookie: str):
        if cookie == "0":
            cookie = str(hash(time.time()))
            self.set_headers("Set-Cookie", cookie)
        else:
            self.set_headers("Cookie", cookie)

    def delete_charset(self, v: str):
        for index, value in enumerate(self.head_normal):
            if value == v:
                self.head_normal.pop(index)
                return
