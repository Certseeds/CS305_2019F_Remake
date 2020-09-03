#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-20 12:53:45 
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

import asyncio
import mimetypes
import os
import urllib.parse

from lab06.src.lab06_02_http_response import *
from lab06.src.lab06_02_http_response_file import http_response_file
from lab06.src.lab06_02_http_response_path import http_response_path
from lab06.src.lab06_02_http_response_wrong import http_response_wrong

server_address: str = '127.0.0.1'
server_port: int = 11456
accept_state: Tuple[str, str] = ('GET', 'HEAD')
cookie_loca: Dict[str, str] = {}


async def once(reader, writer):
    data: bytes = await reader.read(0x3f3f)
    if data == b'':  # chromium的浏览器会发空的包
        return
    datas: List[str] = data.decode().split('\r\n')
    request_line: List[str] = datas[0].split(' ')
    range_begin: int = 0
    range_length: int = 0
    use_range: bool = False
    have_cookie: bool = False
    cookie: str = "0"
    for i in datas:
        if i.split(':')[0] == 'Range':
            # 处理Range
            use_range = True
            range_bytes_1: str = i.split(':')[1].strip()[6:]
            range_begin = int(range_bytes_1.split('-')[0])
            try:
                range_length = int(range_bytes_1.split('-')[1]) - range_begin + 1
            except ValueError:
                range_length = -1
        elif i.split(':')[0] == 'Cookie':
            cookie = i.split(':')[1].strip()
            have_cookie = True

    method, path, http_version = \
        urllib.parse.unquote(request_line[0]), \
        urllib.parse.unquote(request_line[1]), \
        urllib.parse.unquote(request_line[2])  # 避免被空格等干扰
    path += ('/' if path[-1] != '/' else '')
    root_path: str = '.' + path
    will_return: http_response
    # 本处逻辑为先判断 state, 然后按类别分别处理，最后统一返回
    if method not in accept_state:
        will_return = http_response_wrong(405)
    else:
        if os.path.isdir(root_path):
            last_time: str = "/"
            if root_path == './' and have_cookie:
                try:
                    last_time: str = cookie_loca[cookie]
                except KeyError:
                    last_time: str = "/"
            cookie_loca[cookie] = path
            os.chdir(root_path)
            will_return = http_response_path(root_path, method, os.listdir(), have_cookie, last_time)
            os.chdir(os.path.dirname(__file__))
        elif os.path.isfile(root_path[0:-1]):
            file_name: str = root_path[0:-1]  # is file
            file_type: str = mimetypes.guess_type(file_name)[0]
            will_return: http_response_file = http_response_file(file_name, method, file_type)
            will_return.get_file(file_name, range_begin, range_length, use_range)
        else:
            will_return = http_response_wrong(404)
    will_return.set_cookie(cookie)
    writer.write(will_return.get_response())
    try:
        await writer.drain()
    except BrokenPipeError:
        pass
    writer.close()


def server():
    echo_loop = asyncio.get_event_loop()
    server = asyncio.start_server(once, host=server_address, port=server_port, loop=echo_loop)
    serv = echo_loop.run_until_complete(server)
    try:
        echo_loop.run_forever()
    except KeyboardInterrupt:
        pass

    serv.close()
    echo_loop.run_until_complete(serv.wait_closed())
    echo_loop.close()


if __name__ == "__main__":
    try:
        server()
    except KeyboardInterrupt:
        exit()
