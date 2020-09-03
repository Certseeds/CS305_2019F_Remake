"""Example Topology Manager Template
CSCI1680

This class is meant to serve as an example for how you can track the
network's topology from netwokr events.

**You are not required to use this file**: feel free to extend it,
change its structure, or replace it entirely.

"""

from ryu.topology.switches import Port, Switch, Link


class Device():
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


class TMHost(Device):
    """Representation of a host, extends Device

    This class is a wrapper around the Ryu Host object,
    which contains information about the switch port to which
    the host is connected
    """

    def __init__(self, name, host):
        super(TMHost, self).__init__(host)

        self.host = host
        # TODO:  Add more attributes as necessary

    def get_mac(self):
        return self.host.mac

    def get_ips(self):
        return self.host.ipv4

    def get_port(self):
        """Return Ryu port object for this host"""
        return self.host.port

    # . . .


class TopoManager():
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
