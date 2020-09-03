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


class TMSwitch(Device):
    """Representation of a switch, extends Device

    This class is a wrapper around the Ryu Switch object,
    which contains information about the switch's ports
    """

    def __init__(self, name, switch):
        super(TMSwitch, self).__init__(name)

        self.switch = switch
        # TODO:  Add more attributes as necessary

    def get_dpid(self):
        """Return switch DPID"""
        return self.switch.dp.id

    def get_ports(self):
        """Return list of Ryu port objects for this switch
        """
        return self.switch.ports

    def get_dp(self):
        """Return switch datapath object"""
        return self.switch.dp

    # . . .
