#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-20 12:37:30 
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
import socket

hello = [b'HTTP/1.0 200 OK\r\n',
         b'Connection: close'
         b'Content-Type:text/html; charset=utf-8\r\n',
         b'\r\n',
         b'<html><body>Hello World!<body></html>\r\n',
         b'\r\n']
err404 = [b'HTTP/1.0 404 Not Found\r\n',
          b'Connection: close'
          b'Content-Type:text/html; charset=utf-8\r\n',
          b'\r\n',
          b'<html><body>404 Not Found<body></html>\r\n',
          b'\r\n']


def web():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8080))
    sock.listen(10)
    while True:
        conn, address = sock.accept()
        data = conn.recv(2048).decode().split('\r\n')
        print(data[0].split(' '))
        res = err404
        if data[0].split(' ')[1] == '/':
            res = hello
        for line in res:
            conn.send(line)
        conn.close()


if __name__ == "__main__":
    try:
        web()
    except KeyboardInterrupt:
        exit()
