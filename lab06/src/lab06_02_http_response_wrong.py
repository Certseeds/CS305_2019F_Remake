#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-21 11:28:09 
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


class http_response_wrong(http_response):
    def __init__(self, code: int):
        super().__init__()
        self.body: List[str] = ['<!DOCTYPE html>\r\n', "<html>\r\n<body>{} {}</body>\r\n</html>\r\n"]
        self.set_state_code_msg(code)

    def set_state_code_msg(self, code: int):
        try:
            msg: str = state_code_msg[code]
        except KeyError:
            msg: str = "Wrong Code"
        self.head_normal[0] = self.head_normal[0].format(code, msg)
        self.body[1] = self.body[1].format(code, msg)

    def get_response(self) -> bytes:
        return get_string(self.head_normal, self.body).encode()


if __name__ == '__main__':
    hw: http_response_wrong = http_response_wrong(405)
    temp: bytes = hw.get_response()
    x: int = 1
