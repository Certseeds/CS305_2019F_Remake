#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-20 12:50:30 
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
from typing import List

illegal: List[bytes] = [b'\xff\xf4\xff\xfd\x06', b'exit']


def echo():
    server_address = '127.0.0.1'
    server_port = 5555
    echo_loop = asyncio.get_event_loop()
    server = asyncio.start_server(thinkpeach, server_address, server_port, loop=echo_loop)
    serv = echo_loop.run_until_complete(server)
    try:
        echo_loop.run_forever()
    except KeyboardInterrupt:
        pass

    serv.close()
    echo_loop.run_until_complete(serv.wait_closed())
    echo_loop.close()


async def thinkpeach(reader, writer):
    while True:
        data = await reader.read(2048)
        if data and data not in illegal:
            datas = data.decode().split('\r\n')
            writer.write(data)
            for i in datas:
                print(i)
            await writer.drain()
        else:
            writer.close()
            print("this process jump out")
            return

if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
