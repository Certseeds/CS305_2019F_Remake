#!/usr/bin/env python3
# coding=utf-8
'''
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-02 09:49:59
@LastEditors: nanoseeds
@LastEditTime: 2020-07-12 17:13:53
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
import sys

from lab07.src.config import *
from lab07.src.rdt_socket import rdt_socket

BUFFer_size: int = 4096
client = rdt_socket()


def main():
    client.sendall(MESSAGE)

if __name__ == "__main__":
    with open('alice.txt', mode='r') as alice:
        MESSAGE = alice.read()
    client.connect(SERVER_Tuple)
    main()
    client.close()
    sys.exit(0)