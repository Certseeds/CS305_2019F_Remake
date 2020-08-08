#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-20 12:54:37 
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
import os
import urllib.parse
import html
from lab06.src.lab06_02_http_response import *


class http_response_path(http_response):
    def __init__(self, root_path: str, method: str, dir: List[str], have_cookie: bool, last_posi: str):
        super().__init__()
        self.root_path: str = root_path
        self.method: str = method
        self.body_head: List[str] = ['<!DOCTYPE html>\r\n',
                                     '<html>\r\n',
                                     '<head><title>Index of {}</title></head>\r\n',
                                     '<body bgcolor="white"> \r\n',
                                     '<h1>Index of {}</h1><hr>\r\n ',
                                     '<pre>\r\n']
        self.file: List[str] = []
        self.dir: List[str] = []
        self.body_default: List[str] = ['</pre>\r\n ',
                                        '<hr> \r\n',
                                        '\r\n']
        self.body_head[2] = self.body_head[2].format(root_path)
        self.body_head[4] = self.body_head[4].format(root_path)
        self.fill_file_dir(dir, have_cookie, last_posi)

    def get_response(self) -> bytes:
        if self.method == 'HEAD':
            return get_string(self.head_normal).encode()
        elif self.method == 'GET':
            return get_string(self.head_normal, self.body_head, self.dir, self.file, self.body_default).encode()

    # void
    def fill_file_dir(self, names: List[str], have_cookie: bool = False, last_posi: str = ''):
        for i in names:
            if os.path.isfile(i):
                self.file.append("<a href=\"{}\">{}</a><br\r\n />".format(urllib.parse.quote(i), html.escape(i)))
            elif os.path.isdir(i):
                self.dir.append(
                    "<a href=\"{}\">{}</a><br\r\n />".format(urllib.parse.quote(i + '/'), html.escape(i + '/')))
        if self.root_path != './':
            self.dir.insert(0, "<a href=\"{}\">{}</a><br\r\n>".format('../', "../"))
        elif have_cookie and last_posi != "/":
            self.head_normal[0] = "HTTP/1.0 {} {}\r\n".format(302, state_code_msg[302])
            self.set_headers("Location", "{}".format(last_posi))