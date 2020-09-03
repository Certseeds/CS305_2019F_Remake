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
from project.Device import Device
from project.TMHost import TMHost
from project.TMSwitch import TMSwitch


class TopoManager:
    """
    Example class for keeping track of the network topology

    """

    def __init__(self):
        # TODO:  Initialize some data structures
        self.all_devices = []
        pass

    def add_switch(self, sw):
        name = "switch_{}".format(sw.dp.id)
        switch = TMSwitch(name, sw)

        self.all_devices.append(switch)

        # TODO:  Add switch to some data structure(s)

    def add_host(self, h):
        name = "host_{}".format(h.mac)
        host = TMHost(name, h)

        self.all_devices.append(host)

        # TODO:  Add host to some data structure(s)

    # . . .
