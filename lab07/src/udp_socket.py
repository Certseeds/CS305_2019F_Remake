#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-02 09:49:59
@LastEditors: nanoseeds
@LastEditTime: 2020-07-04 15:27:00
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
import random
import time
from abc import abstractmethod
from socket import *
from typing import List, Tuple


# 继承的是UDP, 另外还附加了不稳定性
def _corrupt(data: bytes) -> bytes:
    raw: List[int] = list(data)
    for i in range(0, random.randint(1, 3)):  # [1,3]个bit错误
        pos: int = random.randint(0, len(raw) - 1)
        raw[pos] = random.randint(0, 255)
    return bytes(raw)


class UDPsocket(socket):
    def __init__(self, loss_rate: float = 0.1, corruption_rate: float = 0.3,
                 delay_rate: float = 0.1, delay_time: float = 0.5) -> None:
        super().__init__(AF_INET, SOCK_DGRAM)  # UDP
        self.setblocking(False)  # 非阻塞模式
        self.loss_rate: float = loss_rate  # 丢失率
        self.corruption_rate: float = corruption_rate  # 错误率
        self.delay_rate: float = delay_rate  # 延时率
        self.delay_time: float = delay_time  # 延时时长

    def recvfrom(self, bufsize: int, flags: int = ...) -> Tuple[bytes, Tuple[str, int]]:
        """
        需要注意到的是,因为udp是基于包的协议,所以bufsize指的是收到一个包的最大长度.
        在本机上client-server通信,udp丢包率较低可忽略,
        所以,recvfrom的每一个包默认视作可收到,再有bufsize做截断.
        而且,这里的丢包也不是完全接收不到,只是接收到了空包
        """
        data: bytes
        addr: Tuple[str, int]  # example: ('127.0.0.1',random.randint(10000,65535))
        data, addr = super().recvfrom(bufsize)
        # 也有可能收不到
        if random.random() < self.delay_rate:  # 模拟延迟现象
            time.sleep(self.delay_time)
            print("delay happen")
            return data, addr
        if random.random() < self.loss_rate:  # 模拟丢包,重新侦听
            print("mis happen")
            return self.recvfrom(bufsize)
            # return b'', ('0.0.0.0', 0)
        if random.random() < self.corruption_rate:  # 模拟随机位损坏
            print("bit change")
            return _corrupt(data), addr
        return data, addr  # 无事发生

    def sendto(self, data: bytes, address: Tuple[str, int]) -> int:
        self.setblocking(False)
        will_return: int = super().sendto(data, address)
        return will_return

    # 这个函数不应该被使用,这一层只负责封装UDP为不稳定的UDP,不做其他的处理-
    @abstractmethod
    def recv(self, bufsize: int, flags: int = ...) -> bytes:  # 封装recv
        pass
        # self.setblocking(False)
        # data, addr = self.recvfrom(bufsize, flags)
        # return data

    # i dont know why this one appear in there,
    # 一个UDP为什么能用send,还不指定地址的发出去
    @abstractmethod
    def send(self, data: bytes, flags: int = ...) -> int:
        pass
        # self.setblocking(False)
        # will_return: int = super().send(data, flags)
        # return will_return

    @abstractmethod
    def sendall(self, data: bytes, flags: int = ...) -> None:
        pass

# UDP ->UDPsocket ->TCP_socket
