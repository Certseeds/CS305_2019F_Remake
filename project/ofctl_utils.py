# Copyright (C) 2013 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numbers
import socket
import struct

from ryu.exception import OFPUnknownVersion
from ryu.lib import dpid as dpid_lib
from ryu.lib import hub
from ryu.lib import mac as mac_lib
from ryu.lib import addrconv
from ryu.lib.packet import arp
from ryu.lib.packet import ethernet
from ryu.lib.packet import icmp
from ryu.lib.packet import ipv4
from ryu.lib.packet import packet
from ryu.lib.packet import vlan
from ryu.ofproto import ether
from ryu.ofproto import inet
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_2
from ryu.ofproto import ofproto_v1_3

UINT16_MAX = 0xffff
UINT32_MAX = 0xffffffff
UINT64_MAX = 0xffffffffffffffff

ETHERNET = ethernet.ethernet.__name__
VLAN = vlan.vlan.__name__
IPV4 = ipv4.ipv4.__name__
ARP = arp.arp.__name__
ICMP = icmp.icmp.__name__

DEFAULT_TTL = 64
OFP_REPLY_TIMER = 1.0

MAX_SUSPENDPACKETS = 50  # Threshold of the packet suspends thread count.

VLANID_NONE = 0
VLANID_MIN = 2
VLANID_MAX = 4094


class OfCtl(object):
    """

    To use, create an OfCtl object by calling Ofctl.factory with a the datapath object returned by
    a switch event.
    """
    _OF_VERSIONS = {}

    @staticmethod
    def register_of_version(version):
        def _register_of_version(cls):
            OfCtl._OF_VERSIONS.setdefault(version, cls)
            return cls
        return _register_of_version

    @staticmethod
    def factory(dp, logger):
        """
        Create an OfCtl object
        Arguments:
        dp       -- Switch datapath object
        logger   -- RyuApp logger instance
        """
        of_version = dp.ofproto.OFP_VERSION
        if of_version in OfCtl._OF_VERSIONS:
            ofctl = OfCtl._OF_VERSIONS[of_version](dp, logger)
        else:
            raise OFPUnknownVersion(version=of_version)

        return ofctl

    def __init__(self, dp, logger):
        super(OfCtl, self).__init__()
        self.dp = dp
        self.sw_id = {'sw_id': dpid_lib.dpid_to_str(dp.id)}
        self.logger = logger

    def set_sw_config_for_ttl(self):
        # OpenFlow v1_2/1_3.
        pass

    def set_flow(self, cookie, priority, dl_type=0, dl_dst=0, dl_vlan=0,
                 nw_src=0, src_mask=32, nw_dst=0, dst_mask=32,
                 nw_proto=0, idle_timeout=0, actions=None):
        """
        Send a message to install a flow on this datapath
        The following arguments specify match criteria:
        cookie       -- Opaque identifier to reference this rule
        priority     -- Rule priority number
        dl_type      -- EtherType
        dl_dst       -- Ethernet destination address
        dl_vlan      -- VLAN ID (default 0)
        nw_src       -- IP source
        src_mask     -- IP source mask (default /32)
        nw_dst       -- IP destination
        dst_mask     -- IP destination mask (default /32)
        nw_proto     -- IP protocol value
        Other arguments:
        idle_timeout  -- Idle timeout (default 0)
        actions       -- List of actions to apply on match
        """
        # Abstract method
        raise NotImplementedError()

    def delete_flow(self, cookie=0, priority=0, match=None):
        """
        Delete a flow matching the following criteria
        Arguments:
        cookie       -- Cookie referencing this flow or set of flows
                        (default 0)
        priority     -- Priority value for this flow (default 0)
        match        -- Match criteria for deletion
                        (defaults to all)

        NOTE:  OpenFlow 1.0 does not support deletion based on
        the cookie value.  Instead, match fields must be specified.
        """

        # Abstract method
        raise NotImplementedError()

    def send_arp(self, arp_opcode, vlan_id, dst_mac,
                 sender_mac, sender_ip,
                 target_ip, target_mac,
                 src_port, output_port):
        """
        Generate an ARP packet and send it
        Arguments:
        arp_opcode    -- Opcode for message
        vlan_id       -- VLAN identifier, or VLANID_NONE
        dst_mac       -- Destination to send the packet (not an ARP field)
        sender_mac    -- Sender hardware address
        sender_ip     -- Sender protocol address
        target_mac    -- Target hardware address
        target_ip     -- Target protocol address
        src_port      -- Source port number for sending message (can be OFPP_CONTROLLER)
        output_port   -- Outgoing port number to send message
        """

        if vlan_id != VLANID_NONE:
            ether_proto = ether.ETH_TYPE_8021Q
            pcp = 0
            cfi = 0
            vlan_ether = ether.ETH_TYPE_ARP
            v = vlan.vlan(pcp, cfi, vlan_id, vlan_ether)
        else:
            ether_proto = ether.ETH_TYPE_ARP
        hwtype = 1
        arp_proto = ether.ETH_TYPE_IP
        hlen = 6
        plen = 4

        pkt = packet.Packet()
        e = ethernet.ethernet(dst_mac, sender_mac, ether_proto)
        a = arp.arp(hwtype, arp_proto, hlen, plen, arp_opcode,
                    sender_mac, sender_ip, target_mac, target_ip)
        pkt.add_protocol(e)
        if vlan_id != VLANID_NONE:
            pkt.add_protocol(v)
        pkt.add_protocol(a)
        pkt.serialize()

        # Send packet out
        self.send_packet_out(src_port, output_port, pkt.data, data_str=str(pkt))

    def send_icmp(self, in_port, protocol_list, vlan_id, icmp_type,
                  icmp_code, icmp_data=None, msg_data=None, src_ip=None):
        # Generate ICMP reply packet
        csum = 0
        offset = ethernet.ethernet._MIN_LEN

        if vlan_id != VLANID_NONE:
            ether_proto = ether.ETH_TYPE_8021Q
            pcp = 0
            cfi = 0
            vlan_ether = ether.ETH_TYPE_IP
            v = vlan.vlan(pcp, cfi, vlan_id, vlan_ether)
            offset += vlan.vlan._MIN_LEN
        else:
            ether_proto = ether.ETH_TYPE_IP

        eth = protocol_list[ETHERNET]
        e = ethernet.ethernet(eth.src, eth.dst, ether_proto)

        ip = protocol_list[IPV4]

        if icmp_data is None and msg_data is not None:
            # RFC 4884 says that we should send "at least 128 octets"
            # if we are using the ICMP Extension Structure.
            # We're not using the extension structure, but let's send
            # up to 128 bytes of the original msg_data.
            #
            # RFC 4884 also states that the length field is interpreted in
            # 32 bit units, so the length calculated in bytes needs to first
            # be divided by 4, then increased by 1 if the modulus is non-zero.
            #
            # Finally, RFC 4884 says, if we're specifying the length, we MUST
            # zero pad to the next 32 bit boundary.
            end_of_data = offset + len(ip) + 128
            ip_datagram = bytearray()
            ip_datagram += msg_data[offset:end_of_data]
            data_len = int(len(ip_datagram) / 4)
            length_modulus = int(len(ip_datagram) % 4)
            if length_modulus:
                data_len += 1
                ip_datagram += bytearray([0] * (4 - length_modulus))
            if icmp_type == icmp.ICMP_DEST_UNREACH:
                icmp_data = icmp.dest_unreach(data_len=data_len,
                                              data=ip_datagram)
            elif icmp_type == icmp.ICMP_TIME_EXCEEDED:
                icmp_data = icmp.TimeExceeded(data_len=data_len,
                                              data=ip_datagram)

        ic = icmp.icmp(icmp_type, icmp_code, csum, data=icmp_data)

        if src_ip is None:
            src_ip = ip.dst
        ip_total_length = ip.header_length * 4 + ic._MIN_LEN
        if ic.data is not None:
            ip_total_length += ic.data._MIN_LEN
            if ic.data.data is not None:
                ip_total_length += + len(ic.data.data)
        i = ipv4.ipv4(ip.version, ip.header_length, ip.tos,
                      ip_total_length, ip.identification, ip.flags,
                      ip.offset, DEFAULT_TTL, inet.IPPROTO_ICMP, csum,
                      src_ip, ip.src)

        pkt = packet.Packet()
        pkt.add_protocol(e)
        if vlan_id != VLANID_NONE:
            pkt.add_protocol(v)
        pkt.add_protocol(i)
        pkt.add_protocol(ic)
        pkt.serialize()

        # Send packet out
        self.send_packet_out(in_port, self.dp.ofproto.OFPP_IN_PORT,
                             pkt.data, data_str=str(pkt))

    def send_packet_out(self, in_port, output, data, data_str=None):
        actions = [self.dp.ofproto_parser.OFPActionOutput(output, 0)]
        self.dp.send_packet_out(buffer_id=UINT32_MAX, in_port=in_port,
                                actions=actions, data=data)
        # TODO: Packet library convert to string
        # if data_str is None:
        #     data_str = str(packet.Packet(data))
        # self.logger.debug('Packet out = %s', data_str, extra=self.sw_id)

    def set_normal_flow(self, cookie, priority):
        out_port = self.dp.ofproto.OFPP_NORMAL
        actions = [self.dp.ofproto_parser.OFPActionOutput(out_port, 0)]
        self.set_flow(cookie, priority, actions=actions)

    def set_packetin_flow(self, cookie, priority, dl_type=0, dl_dst=0,
                          dl_vlan=0, dst_ip=0, dst_mask=32, nw_proto=0):
        miss_send_len = UINT16_MAX
        actions = [self.dp.ofproto_parser.OFPActionOutput(
            self.dp.ofproto.OFPP_CONTROLLER, miss_send_len)]
        self.set_flow(cookie, priority, dl_type=dl_type, dl_dst=dl_dst,
                      dl_vlan=dl_vlan, nw_dst=dst_ip, dst_mask=dst_mask,
                      nw_proto=nw_proto, actions=actions)

    def send_stats_request(self, stats, waiters):
        self.dp.set_xid(stats)
        waiters_per_dp = waiters.setdefault(self.dp.id, {})
        event = hub.Event()
        msgs = []
        waiters_per_dp[stats.xid] = (event, msgs)
        self.dp.send_msg(stats)

        try:
            event.wait(timeout=OFP_REPLY_TIMER)
        except hub.Timeout:
            del waiters_per_dp[stats.xid]

        return msgs


@OfCtl.register_of_version(ofproto_v1_0.OFP_VERSION)
class OfCtl_v1_0(OfCtl):

    def __init__(self, dp, logger):
        super(OfCtl_v1_0, self).__init__(dp, logger)

    def get_packetin_inport(self, msg):
        return msg.in_port

    def get_all_flow(self, waiters):
        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser

        match = ofp_parser.OFPMatch(ofp.OFPFW_ALL, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0)
        stats = ofp_parser.OFPFlowStatsRequest(self.dp, 0, match,
                                               0xff, ofp.OFPP_NONE)
        return self.send_stats_request(stats, waiters)

    def set_flow(self, cookie, priority, dl_type=0, dl_dst=0, dl_vlan=0,
                 nw_src=0, src_mask=32, nw_dst=0, dst_mask=32,
                 nw_proto=0, idle_timeout=0, actions=None):

        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser
        cmd = ofp.OFPFC_ADD

        # Match
        wildcards = ofp.OFPFW_ALL
        if dl_type:
            wildcards &= ~ofp.OFPFW_DL_TYPE
        if dl_dst:
            wildcards &= ~ofp.OFPFW_DL_DST
        if dl_vlan:
            wildcards &= ~ofp.OFPFW_DL_VLAN
        if nw_src:
            v = (32 - src_mask) << ofp.OFPFW_NW_SRC_SHIFT | \
                ~ofp.OFPFW_NW_SRC_MASK
            wildcards &= v
            nw_src = ipv4_text_to_int(nw_src)
        if nw_dst:
            v = (32 - dst_mask) << ofp.OFPFW_NW_DST_SHIFT | \
                ~ofp.OFPFW_NW_DST_MASK
            wildcards &= v
            nw_dst = ipv4_text_to_int(nw_dst)
        if nw_proto:
            wildcards &= ~ofp.OFPFW_NW_PROTO

        match = ofp_parser.OFPMatch(wildcards, 0, 0, dl_dst, dl_vlan, 0,
                                    dl_type, 0, nw_proto,
                                    nw_src, nw_dst, 0, 0)
        actions = actions or []

        m = ofp_parser.OFPFlowMod(self.dp, match, cookie, cmd,
                                  idle_timeout=idle_timeout,
                                  priority=priority, actions=actions)
        self.dp.send_msg(m)

    def delete_flow(self, cookie=0, priority=0, match=None):
        cmd = self.dp.ofproto.OFPFC_DELETE
        actions = []

        ofp_parser = self.dp.ofproto_parser

        flow_mod = self.dp.ofproto_parser.OFPFlowMod(
            self.dp, match=match, cookie=cookie, command=cmd, priority=priority, actions=actions)
        self.dp.send_msg(flow_mod)


class OfCtl_after_v1_2(OfCtl):

    def __init__(self, dp, logger):
        super(OfCtl_after_v1_2, self).__init__(dp, logger)

    def set_sw_config_for_ttl(self):
        pass

    def get_packetin_inport(self, msg):
        in_port = self.dp.ofproto.OFPP_ANY
        for match_field in msg.match.fields:
            if match_field.header == self.dp.ofproto.OXM_OF_IN_PORT:
                in_port = match_field.value
                break
        return in_port

    def get_all_flow(self, waiters):
        pass

    def set_flow(self, cookie, priority, dl_type=0, dl_dst=0, dl_vlan=0,
                 nw_src=0, src_mask=32, nw_dst=0, dst_mask=32,
                 nw_proto=0, idle_timeout=0, actions=None):
        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser
        cmd = ofp.OFPFC_ADD

        # Match
        match = ofp_parser.OFPMatch()
        if dl_type:
            match.set_dl_type(dl_type)
        if dl_dst:
            match.set_dl_dst(dl_dst)
        if dl_vlan:
            match.set_vlan_vid(dl_vlan)
        if nw_src:
            match.set_ipv4_src_masked(ipv4_text_to_int(nw_src),
                                      mask_ntob(src_mask))
        if nw_dst:
            match.set_ipv4_dst_masked(ipv4_text_to_int(nw_dst),
                                      mask_ntob(dst_mask))
        if nw_proto:
            if dl_type == ether.ETH_TYPE_IP:
                match.set_ip_proto(nw_proto)
            elif dl_type == ether.ETH_TYPE_ARP:
                match.set_arp_opcode(nw_proto)

        # Instructions
        actions = actions or []
        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS,
                                                 actions)]

        m = ofp_parser.OFPFlowMod(self.dp, cookie, 0, 0, cmd, idle_timeout,
                                  0, priority, UINT32_MAX, ofp.OFPP_ANY,
                                  ofp.OFPG_ANY, 0, match, inst)
        self.dp.send_msg(m)

    def set_routing_flow(self, cookie, priority, outport, dl_vlan=0,
                         nw_src=0, src_mask=32, nw_dst=0, dst_mask=32,
                         src_mac=0, dst_mac=0, idle_timeout=0, dec_ttl=False):
        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser

        dl_type = ether.ETH_TYPE_IP

        actions = []
        if dec_ttl:
            actions.append(ofp_parser.OFPActionDecNwTtl())
        if src_mac:
            actions.append(ofp_parser.OFPActionSetField(eth_src=src_mac))
        if dst_mac:
            actions.append(ofp_parser.OFPActionSetField(eth_dst=dst_mac))
        if outport is not None:
            actions.append(ofp_parser.OFPActionOutput(outport, 0))

        self.set_flow(cookie, priority, dl_type=dl_type, dl_vlan=dl_vlan,
                      nw_src=nw_src, src_mask=src_mask,
                      nw_dst=nw_dst, dst_mask=dst_mask,
                      idle_timeout=idle_timeout, actions=actions)

    def delete_flow(self, cookie, priority=0, match=None):
        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser

        if match is None:
            match = ofp_parser.OFPMatch()

        cmd = ofp.OFPFC_DELETE
        cookie_mask = UINT64_MAX
        inst = []

        flow_mod = ofp_parser.OFPFlowMod(self.dp, cookie, cookie_mask, 0, cmd,
                                         0, 0, 0, UINT32_MAX, ofp.OFPP_ANY,
                                         ofp.OFPG_ANY, 0, match, inst)
        self.dp.send_msg(flow_mod)
        self.logger.info('Delete flow [cookie=0x%x]', cookie, extra=self.sw_id)


@OfCtl.register_of_version(ofproto_v1_2.OFP_VERSION)
class OfCtl_v1_2(OfCtl_after_v1_2):

    def __init__(self, dp, logger):
        super(OfCtl_v1_2, self).__init__(dp, logger)

    def set_sw_config_for_ttl(self):
        flags = self.dp.ofproto.OFPC_INVALID_TTL_TO_CONTROLLER
        miss_send_len = UINT16_MAX
        m = self.dp.ofproto_parser.OFPSetConfig(self.dp, flags,
                                                miss_send_len)
        self.dp.send_msg(m)
        self.logger.info('Set SW config for TTL error packet in.',
                         extra=self.sw_id)

    def get_all_flow(self, waiters):
        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser

        match = ofp_parser.OFPMatch()
        stats = ofp_parser.OFPFlowStatsRequest(self.dp, 0, ofp.OFPP_ANY,
                                               ofp.OFPG_ANY, 0, 0, match)
        return self.send_stats_request(stats, waiters)


@OfCtl.register_of_version(ofproto_v1_3.OFP_VERSION)
class OfCtl_v1_3(OfCtl_after_v1_2):

    def __init__(self, dp, logger):
        super(OfCtl_v1_3, self).__init__(dp, logger)

    def set_sw_config_for_ttl(self):
        packet_in_mask = (1 << self.dp.ofproto.OFPR_ACTION |
                          1 << self.dp.ofproto.OFPR_INVALID_TTL)
        port_status_mask = (1 << self.dp.ofproto.OFPPR_ADD |
                            1 << self.dp.ofproto.OFPPR_DELETE |
                            1 << self.dp.ofproto.OFPPR_MODIFY)
        flow_removed_mask = (1 << self.dp.ofproto.OFPRR_IDLE_TIMEOUT |
                             1 << self.dp.ofproto.OFPRR_HARD_TIMEOUT |
                             1 << self.dp.ofproto.OFPRR_DELETE)
        m = self.dp.ofproto_parser.OFPSetAsync(
            self.dp, [packet_in_mask, 0], [port_status_mask, 0],
            [flow_removed_mask, 0])
        self.dp.send_msg(m)
        self.logger.info('Set SW config for TTL error packet in.',
                         extra=self.sw_id)

    def get_all_flow(self, waiters):
        ofp = self.dp.ofproto
        ofp_parser = self.dp.ofproto_parser

        match = ofp_parser.OFPMatch()
        stats = ofp_parser.OFPFlowStatsRequest(self.dp, 0, 0, ofp.OFPP_ANY,
                                               ofp.OFPG_ANY, 0, 0, match)
        return self.send_stats_request(stats, waiters)


def ip_addr_aton(ip_str, err_msg=None):
    try:
        return addrconv.ipv4.bin_to_text(socket.inet_aton(ip_str))
    except (struct.error, socket.error) as e:
        if err_msg is not None:
            e.message = '%s %s' % (err_msg, e.message)
        raise ValueError(e.message)


def ip_addr_ntoa(ip):
    return socket.inet_ntoa(addrconv.ipv4.text_to_bin(ip))


def mask_ntob(mask, err_msg=None):
    try:
        return (UINT32_MAX << (32 - mask)) & UINT32_MAX
    except ValueError:
        msg = 'illegal netmask'
        if err_msg is not None:
            msg = '%s %s' % (err_msg, msg)
        raise ValueError(msg)


def ipv4_apply_mask(address, prefix_len, err_msg=None):
    assert isinstance(address, str)

    address_int = ipv4_text_to_int(address)
    return ipv4_int_to_text(address_int & mask_ntob(prefix_len, err_msg))


def ipv4_int_to_text(ip_int):
    assert isinstance(ip_int, numbers.Integral)
    return addrconv.ipv4.bin_to_text(struct.pack('!I', ip_int))


def ipv4_text_to_int(ip_text):
    if ip_text == 0:
        return ip_text
    assert isinstance(ip_text, str)
    return struct.unpack('!I', addrconv.ipv4.text_to_bin(ip_text))[0]


def nw_addr_aton(nw_addr, err_msg=None):
    ip_mask = nw_addr.split('/')
    default_route = ip_addr_aton(ip_mask[0], err_msg=err_msg)
    netmask = 32
    if len(ip_mask) == 2:
        try:
            netmask = int(ip_mask[1])
        except ValueError as e:
            if err_msg is not None:
                e.message = '%s %s' % (err_msg, e.message)
            raise ValueError(e.message)
    if netmask < 0:
        msg = 'illegal netmask'
        if err_msg is not None:
            msg = '%s %s' % (err_msg, msg)
        raise ValueError(msg)
    nw_addr = ipv4_apply_mask(default_route, netmask, err_msg)
    return nw_addr, netmask, default_route
