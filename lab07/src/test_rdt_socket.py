#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds
@Organization: SUSTech
@Author: nanoseeds
@Date: 2020-07-04 16:19:59 
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

import random
import string
import unittest

from lab07.src.rdt_socket import *


def random_str(num: int = 10) -> str:
    will_return: str = ''.join(random.choice(string.ascii_letters) for i in range(num))
    return will_return


class MyTestCase(unittest.TestCase):
    def test_produce_packets(self):
        for i in range(10, 100):
            for j in range(10, 100):
                for k in range(10, 100):
                    assert check_sum(produce_packets(header_format, i, j, k, random_str(random.randint(1, 512)))) == 0


if __name__ == '__main__':
    unittest.main()
