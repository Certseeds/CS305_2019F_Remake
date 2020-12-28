<!--
 * @Github: https://github.com/Certseeds/CS305_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 16:06:56
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-09-14 15:43:47
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 14 Details

1. 当堂完成,没有报告.
2. 需要特定硬件.H3C-R810/R830

### Practice1

Build a LAN with $PC_a$, $PC_b$ and a Layer 3 Swith / Router

1. Create two vlan: vlan 'x' and vlan 'y'

2. Configure the vlan and interface:

+ Giga-ethernet interface 'a1' access to vlan 'x' while the Giga-ethernet interface 'b1' access to vlan 'y'

3. Make the connection:

+ Connect the Giga-ethernet interface 'a2' with $PC_a$

+ Connect the Giga-ethernet interface 'b2' with $PC_b$

4. Set $PC_a$ and $PC_b$ as DHCP client.
5. On $PC_a$ , invoke "ping" to test if the link between $PC_a$ and $PC_b$ is reachable, explain the reason
6. Change the connection:

+ Connect the Giga-ethernet interface 'a1' with $PC_a$

+ Connect the Giga-ethernet interface 'b1' with $PC_b$

7. do the test as step 5, what's the testing result, explain the reason
(option)is there anyway to make the link between $PC_a$ and $PC_b$ reachable by not changing
the connection? Try to do it.

### Practice 2

1. Build a LAN with $PC_{a}$,$PC_{b}$ and a Layer3 switch/router.

+ because two PC belongs to the same Lab, so if invoke `ping` on  $PC_{a}$ to reach $PC_{b}$, the result will show the link between  $PC_{a}$ and $PC_{b}$ is OK, they are both reachable in the LAN.

Check the mac-address table on the switch

+ how many items on the switch mac-address table? is it static or dynamic?
+ For every item, is the mac-address belongs to the connected PC or the connected interface of switch?

Using two ways to make the link between  $PC_{a}$ and $PC_{b}$, is broken while not change the connection on them.

### Practice 3

+ Build a LAN with $PC_{a}$, $PC_{b}$ and a Layer3 switch/route
+ Create a vlan-interface, configure its IPv6 address
+ Enable the neighbor discover on the vlan-interface to make the PCs belongs to the vlan got a stateless address
- Could the PC got an IPv6 address? What the length of prefix on the address?
- What 's the difference between this address with IPv6 link address?
- Invoke the 'ping -6' test on $PC_{a}$ to check if $PC_{b}$ is reachable or not, explain the reason.
- (Option) create and enable a DHCPv6 server on the Layer3 switch/Route and test

### Tips for Practice 1

#### Mac-address 

1. you can use command [H3C]:`display mac-address`, [H3C]:`display mac-address aging-time` to get some information about mac-address.
2. you can use command [H3C]:`mac-address static ${mac-address} interface ${PORT_INDEX} vlan ${VLAN_ID}` to make it's state to `Config static`.
3. you can use command [H3C]:`mac-address blackhole  ${mac-address} vlan ${VLAN_ID}` to make it's state to `blackhole`

+ The `blackhole` mac address means while the packets related to the blackhole, they will be dropped, switch will not forward the packets.
+ you can test what will happen if ping a blackhole address.

#### Isolate Port Group

The interfaces which belongs to an isolate group can't reach each other, but can communicate with the interfaces which is not belongs to the isolate group~~(自闭组)~~

+ use command [H3C]:`display port-isolate group` to find groups.
+ use command [H3C-${PORT_INDEX}]:`port-isolate enable` to enable this port to enable this port's port-isolate.
+ PS: default all ports that enable there port-isolate will be add to the same port-isolate group.

### Tips for practice 2

#### IPv6 configuration on Layer 3

Different types of IPv6 address

+ State address : got from DHCP server , global address
+ Stateless address: got by Route Advise, same as private address in IPv4
+ Local link address: with prefix（FE80::/10）as its prefix, this address could be used to communicate with other PC on the local network

Tips: S5110 ethernet interface work on bridge mode, can't got an IPv6 address while the vlan-interface can work on route mode.

#### Got a stateless IPv6 address-1

0. create vlan command

+ [H3C]:`vlan ${Vlan-order}`  then it is create a vlan which order is ${Vlan-order}
+ [H3C-vlan${Vlan-order}]: ` quit` escape from this enviorment, like `cd ..`  
+ [H3C]: `interface vlan-interface ${vlan-order}`

1. Enable an neighbor discover on an IPv6 interface by commands:

+ [H3C-Vlam-Interface${interface_order}]:`ipv6 address ${address_of_ipv6}` 设定IPv6地址
+ [H3C-Vlam-Interface${interface_order}]:`undo ipv6 nd ra halt` (打开ipv6的路由广播功能)
+ [H3C-Vlam-Interface${interface_order}]:`display this`, output the vlan informations.
+ [H3C]:`display ipv6 neighbors all`: 显示IPv6版本的display

2. 更多command:

+ [H3C]:`display ipv6 interface Vlan-interface ${interface-vlan-number}` display 更多信息
+ [H3C]:`display ipv6 fib`, 获取更多信息 

### Tips for R810/R830

1. DHCP server

- Using "undo dhcp server ip-pool pool_name" to remove all the dhcp server ip-pool

2. Interface

- Link-mode: the interface which works under bridge mode is same with the interface of switch. Using "port link-mode bridge" can change the work mode of interface to bridge.
- ID: on S5110,interface number is identify by '1/0/x' while interface of R810/830 is '0/x'

3. Vlan-interface

- While using R810/830, configure the vlan interface, two more configuration is needed:
  + ipv6 nd autoconfig managed-address-flag
  + Ipv6 nd autoconfig other-flag

<style type="text/css">
div{
  text-align: center;
}
div>div {
  text-align: center;
  border-bottom: 1px solid #d9d9d9;
  display: inline-block;
  padding: 2px;
}
div>img{
  border-radius: 0.3125em;
  box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);
}
</style>