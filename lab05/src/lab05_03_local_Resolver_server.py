#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@ChangeDate: 2019-12-23 10:33:34
@LastEditors: nanoseeds
"""
from typing import Any

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
from socket import *
import time
from lab05.src.lab05_03_helper_functions import *
from lab05.src.lab05_03_dns_querys import dns_querys
from lab05.src.lab05_03_dns_querys_answer import dns_querys_answer

"""
首先,本次出现的 八位数组 能够被写为 [0-f][0-f]的形式,每个字符[0-f]可被转写为[0-1]*4,所以八位数组可以被转写为[0-1]*8,而二进制流中的最小单位就是八位数组:[0-f][0-f]
"""
questions_cache: List[List[int]] = []
response_cache: List[dns_querys_answer] = []
prot_number: int = 53
server_address: Tuple[str, int] = ("127.0.0.1", prot_number)
dns_address: Tuple[str, int] = ("114.114.114.114", 53)  # forward query dns address.
Living_time: int = 1024  # 1024 seconds
recv_length: int = 2048
server_socket: socket = socket(AF_INET, SOCK_DGRAM)
dns_socket: socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_address)


def add_for_cache(request_address: Tuple[str, int], request_object: dns_querys):
    dns_socket.sendto(request_object.get_querys_all(), dns_address)
    response, useless_address = dns_socket.recvfrom(recv_length)
    server_socket.sendto(response, request_address)
    questions_cache.append(request_object.get_querys_question())
    response_cache.append(dns_querys_answer(response))
    print("add for cache finish")


def main():
    while True:
        request: bytes
        request_address: Tuple[str, int]
        try:
            request, request_address = server_socket.recvfrom(recv_length)
        except ConnectionResetError:
            print("connect failed, waiting...")
            continue
        request_object: dns_querys = dns_querys(request)
        delete_list: List[int] = []
        for index, value in enumerate(response_cache):
            if value.judge_is_out(live_time=Living_time):
                delete_list.append(index)
        for i in reversed(delete_list):
            questions_cache.pop(i)
            response_cache.pop(i)
        # 判断question是否被client提出过
        temp = request_object.get_querys_question()
        if temp in questions_cache:
            print("in here")
            index_of = questions_cache.index(request_object.get_querys_question())
            response_cache[index_of].HQ = request_object
            if response_cache[index_of].judge_is_out(live_time=Living_time):
                print("it need change")
                questions_cache.pop(index_of)
                response_cache.pop(index_of)
                print("recieve one ")
                add_for_cache(request_address, request_object)
            else:
                print("change no need")
                for index, value in enumerate(response_cache[index_of].ttl):
                    print(value[1], " is the ttl")
                    # 更新ttl
                    return_ttl: int = value[1] - (int(time.time()) - response_cache[index_of].initime)
                    response_cache[index_of].ans_ttls[index] = trans_int_tobit(return_ttl)
                # 传回发送的那边
                server_socket.sendto(response_cache[index_of].get_header_question_answers(), request_address)
        else:
            add_for_cache(request_address, request_object)


if __name__ == '__main__':
    main()
