#!/usr/bin/env python3
# coding=utf-8
"""
@Github: https://github.com/Certseeds/CS305_2019F_Remake
@Organization: SUSTech
@Author: nanoseeds
@LastEditors: nanoseeds
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


class Device:
    """Base class to represent an device in the network.

    Any device (switch or host) has a name (used for debugging only)
    and a set of neighbors.
    """

    def __init__(self, name):
        self.name = name
        self.neighbors = set()

    def add_neighbor(self, dev):
        self.neighbors.add(dev)

    # . . .

    def __str__(self):
        return "{}({})".format(self.__class__.__name__,
                               self.name)
