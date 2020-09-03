#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-02 13:17:41
@LastEditors: nanoseeds
@LastEditTime: 2020-07-12 17:54:28
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
import struct
import traceback
from typing import Tuple

address_tuple = Tuple[str, int]

SERVER_ADDR: str = "127.0.0.1"
SERVER_PORT: int = 23579
SERVER_Tuple: address_tuple = (SERVER_ADDR, SERVER_PORT)
data_format: str = "UTF-8"
header_length: int = 20
header_format: str = "!5L"


def produce_packets(formats: str, bits: int, seq: int, seq_ack: int,
                    data_str: [str, bytes] = "") -> bytes:
    data_bytes: bytes = str_byte_to_str(data_str)
    check_data: int = check_sum(struct.pack(
        formats, bits, seq, seq_ack, len(data_str), 0), data_bytes)
    will_return: bytes = struct.pack(
        formats, bits, seq, seq_ack, len(data_str), check_data) + data_bytes
    assert check_sum(will_return) == 0
    return will_return


def str_byte_to_str(data_str: [str, bytes] = "") -> bytes:
    assert isinstance(data_str, (str, bytes)) is True
    data_bytes: bytes = b'0'
    try:
        if isinstance(data_str, str):
            data_bytes = bytes(data_str.encode(data_format))
        elif isinstance(data_str, bytes):
            data_bytes = data_str
    except (AttributeError, UnicodeEncodeError) as e:
        traceback.print_exc()
    return data_bytes

def check_sum(data: bytes, *datas: Tuple[bytes]) -> int:
    sum: int = 0
    for byte in data:
        sum += byte
    for one_data in datas:
        for byte in one_data:
            sum += byte
    sum = -(sum % (1 << 8))
    return sum & 0xFF
