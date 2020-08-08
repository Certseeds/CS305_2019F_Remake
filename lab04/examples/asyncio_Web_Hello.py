#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-20 12:32:12 
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
import asyncio


async def thinkpeach(reader, writer):
    data = await reader.readline()
    '''message = data.decode().split(' ')
    print(data)
    if data == b'\r\n':
       break
    writer.writelines([ b'HTTP/1.0 200 OK\r\n',
                                 b'Content-Type:text/html; charset=utf-8\r\n,'
                                  b'Connection: close\r\n', b'\r\n',
                                  b'<html><body>Hello World!<body></html>\r\n', b'\r\n' ])
    await writer.drain()
    writer.close()'''
    message = data.decode()
    addr = writer.get_extra_info('peername')
    writer.weiter(data)
    await writer.drain()
    writer.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(thinkpeach, '127.0.0.1', 8080, loop=loop)
    server = loop.run_until_complete(coro)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
