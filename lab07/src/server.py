#!/usr/bin/env python3
# coding=utf-8
'''
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-02 09:49:59
@LastEditors: nanoseeds
@LastEditTime: 2020-07-03 13:08:06
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

from lab07.src.config import *
from lab07.src.rdt_socket import rdt_socket

server = rdt_socket()


def main():
    count: int = 0
    while True:
        conn, client = server.accept()
        print("process1 finish")
        data: str
        while True:
            print("{}-------------------".format(count))
            count += 1
            data += conn.recv(2048)
            print("recieved")
            print(data)
            if len(data) < 1:
                # 这里指发空包
                print("break now------------------------------------")
                break
            # conn.send(data)
            print("1 circle over")
            print(time.time())
            print("length of receive is {}".format(len(data)))
    conn.close()


if __name__ == "__main__":
    server.bind(SERVER_Tuple)
    server.listen()
    conn, client = server.accept()
    data = conn.recvall()
    print(len(data))
    conn.close()
