#!/usr/bin/env python2
"""
Custom topologies for project SDN
"""

import sys
import time
import argparse

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.topo import Topo,SingleSwitchTopo,LinearTopo
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel, info


class AssignOneTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        h9 = self.addHost('h9')
        h10 = self.addHost('h10')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        self.addLink(h1, s1)
        self.addLink(h7, s1)
        self.addLink(h8, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h9, s4)
        self.addLink(h10, s4)
        self.addLink(h5, s5)
        self.addLink(h6, s6)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s2, s5)
        self.addLink(s3, s6)


class TriangleTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)


class SomeLoopsTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        self.addLink(h1, s1)
        self.addLink(h2, s5)
        self.addLink(h3, s4)
        self.addLink(h4, s6)
        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s3, s6)
        self.addLink(s2, s5)
        self.addLink(s5, s4)
        self.addLink(s4, s6)
        self.addLink(s6, s1)


class MeshTopo(Topo):
    def __init__(self, n=4, **opts):
        Topo.__init__(self, **opts)
        switches = []
        for i in range(1,n+1):
            h = self.addHost('h%d' % i)
            s = self.addSwitch('s%d' % i)
            self.addLink(h, s)
            switches.append(s)
        for i in range(0,n-1):
            for j in range(i+1,n):
                self.addLink(switches[i], switches[j])


ALL_TOPOLOGIES = {
    "single": SingleSwitchTopo,
    "tree": TreeTopo,
    "linear": LinearTopo,
    "assign1": AssignOneTopo,
    "triangle": TriangleTopo,
    "mesh": MeshTopo,
    "someloops": SomeLoopsTopo,
}


# Mininet CLI command to arping all hosts
# (This is useful to force all hosts to rejoin after restarting the
# controller)
def do_arping_all(self, line):
    for h in self.mn.hosts:
        info('*** Sending ARPing from host %s\n' % (h.name))
        # Send a "join message", which is a gratuitous ARP
        send_arping(h)


def do_arping(self, line):
    from mininet.log import error
    args = line.split()

    if not args:
        error("Usage:  arping <host>\n")
    else:
        host = args[0]
        if host not in self.mn:
            error("Host {} not found in network\n".format(host))
        else:
            send_arping(self.mn[host])


def send_arping(node):
    node.cmd('arping -c 1 -A -I {}-eth0 {}'.format(node.name, node.IP()))


def disable_ipv6(node):
    node.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
    node.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
    node.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", type=str,
                        default="info")

    subparsers = parser.add_subparsers(dest="command")
    sp_cmds = {t: subparsers.add_parser(t) for t in ALL_TOPOLOGIES.keys()}

    sp_cmds["single"].add_argument("nodes", type=int)
    sp_cmds["tree"].add_argument("depth", type=int)
    sp_cmds["linear"].add_argument("nodes", type=int)
    sp_cmds["mesh"].add_argument("nodes", type=int)

    args = parser.parse_args()

    setLogLevel(args.log_level)

    if args.command == "single":
        topo = ALL_TOPOLOGIES["single"](args.nodes)
    elif args.command == "tree":
        topo = ALL_TOPOLOGIES["tree"](args.depth)
    elif args.command == "linear":
        topo = ALL_TOPOLOGIES["linear"](args.nodes)
    elif args.command == "mesh":
        topo = ALL_TOPOLOGIES["mesh"](args.nodes)
    else:
        topo = ALL_TOPOLOGIES[args.command]()

    # Add custom CLI commands
    CLI.do_arping_all = do_arping_all
    CLI.do_arping = do_arping

    # Create the network
    net = Mininet(topo=topo, autoSetMacs=True, controller=RemoteController)

    # Disable IPv6 on the hosts and switches, since we are not using it
    # This avoids suprious ICMPv6 messages that complicate link discovery
    for h in net.hosts:
        disable_ipv6(h)

    for h in net.switches:
        disable_ipv6(h)

    # Run network
    net.start()

    # Wait for the network to initialize
    # (This ensures the controller knows about all switches
    # before the hosts send join requests)
    time.sleep(1)

    # Tell each host to join the network
    for h in net.hosts:
        # Send a "join message", which is a gratuitous ARP
        info('*** Sending ARPing from host %s\n' % (h.name))
        send_arping(h)
    CLI( net )
    net.stop()


if __name__ == '__main__':
    main()
