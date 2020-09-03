#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-06-25 18:13:53 
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
import struct


class DNSHeader:
    Struct = struct.Struct('!6H')

    def __init__(self):
        self.__dict__ = {
            field: None
            for field in
            ('ID', 'QR', 'OpCode', 'AA', 'TC', 'RD', 'RA', 'Z', 'RCode', 'QDCount', 'ANCount', 'NSCount', 'ARCoun')}

    def parse_header(self, data):
        self.ID, misc, self.QDCount, self.ANcount, self.NScount, self.NScount = DNSHeader.Struct.unpack_from(data)
        self.QR = (misc & 0x8000) != 0  # [0:0]
        self.OpCode = (misc & 0x7800) >> 11  # [1:4]
        self.AA = (misc & 0x0400) != 0  # [5:5]
        self.TC = (misc & 0x200) != 0  # [6:6]
        self.RD = (misc & 0x100) != 0  # [7:7]
        self.RA = (misc & 0x80) != 0  # [8:8]
        self.Z = (misc & 0x70) >> 4  # [9:9]

        # Never used self.RCode = misc & 0xF

    def __str__(self):
        return '<DNSHeader {}>'.format(str(self.__dict__))
