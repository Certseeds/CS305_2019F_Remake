#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-18 11:03:47 
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
from time import time
from socket import *

client: socket = socket(AF_INET, SOCK_STREAM)
SERVER_ADDR: str = "127.0.0.1"
SERVER_PORT: int = 23579
SERVER_Tuple = (SERVER_ADDR, SERVER_PORT)
MESSAGE: bytes


def main():
    for i in range(1, 10):
        client.send(MESSAGE[i * 500:i * 500 + 500])
        print("send finish")
        print("1 circle over")
    for i in range(1, 10):
        data = client.recv(500)
        print("recieve finish")
        print(time())
        print(len(data))


if __name__ == "__main__":
    with open('./../src/alice.txt', mode='r') as alice:
        MESSAGE = bytes(alice.read(), encoding='UTF-8')
    client.connect(SERVER_Tuple)
    main()
    client.close()
