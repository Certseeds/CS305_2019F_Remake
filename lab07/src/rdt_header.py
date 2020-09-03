#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-12 17:46:45 
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
from lab07.src.config import *


class rdt_header(object):

    def __init__(self, bits: int, seq_num: int, ack_num: int, data_str: [str, bytes] = ""):
        self.bits: int = bits
        self.seq_num: int = seq_num
        self.ack_num: int = ack_num
        self.length: int = len(data_str)

    @classmethod
    def unpack(cls, data_bytes: bytes) -> 'rdt_header':
        if len(data_bytes) < header_length:
            return cls(0, -1, -1)
        assert len(data_bytes) >= header_length
        bits, seq_num, ack_num, length, temp = struct.unpack(header_format, data_bytes[0:header_length])
        will_return: rdt_header = cls(bits, seq_num, ack_num)
        will_return.length = length
        return will_return

    def to_bytes(self) -> bytes:
        return produce_packets(header_format, self.bits, self.seq_num, self.ack_num, "")

    def equal(self, **args) -> bool:
        will_return = True
        if 'bits' in args:
            will_return = will_return and args['bits'] == self.bits
        if 'seq_num' in args:
            will_return = will_return and args['seq_num'] == self.seq_num
        if 'ack_num' in args:
            will_return = will_return and args['ack_num'] == self.ack_num
        if 'length' in args:
            will_return = will_return and args['length'] == self.length
        return will_return

    def __str__(self):
        return "bits:{} seq:{} ack:{} length:{}".format(str(self.bits), str(self.seq_num), str(self.ack_num),
                                                        str(self.length))


if __name__ == '__main__':
    head = rdt_header(7, 0, 0, '12345')
    assert head.equal(bits=7, seq_num=0, ack_num=0, length=5)
    head2 = rdt_header.unpack(b'\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05')
    assert head2.equal(bits=1, seq_num=2, ack_num=3, length=4)
