#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-18 11:03:55 
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
import time
from socket import *

server: socket = socket(AF_INET, SOCK_STREAM)
SERVER_ADDR: str = "127.0.0.1"
SERVER_PORT: int = 23579
SERVER_Tuple = (SERVER_ADDR, SERVER_PORT)
MESSAGE: bytes


def main():
    count: int = 0
    while True:
        client, address = server.accept()
        while True:
            data = client.recv(600)
            time.sleep(1)
            if data != b'':
                print(data)
                print(len(data))
                print("process1 finish")
                print("{}-------------------".format(count))
                count += 1
                client.send(data)
    conn.close()


if __name__ == "__main__":
    server.bind(SERVER_Tuple)
    server.listen()
    main()
