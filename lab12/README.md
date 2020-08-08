<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-08-08 22:19:05
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-08 22:59:58
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 12 Details
注:下述练习需要硬件

### Practice1
Look up the info of router
  + the device and memory
  + the interface( port mode, port number, bandwidth of port, link type, ipaddress )
  + the service (default DHCP server)

Configuration
  + Rename the router with "CS305_yourID"
  + Change the port-mode of interface
  + Configure ip address on interface with different subnet
  + Create new DHCP server ip-pool, set its network, gateway-list and address-range
  + Reset the MTU of a interface

### Practice2
+ Create a internet with two PCs($PC_a$ and $PC_b$) and a Router
+ Configure the network to make:
  - $PC_a$ belongs to subnet1, $PC_b$ belongs to subnet2, Router connect subnet1 and subnet2
+ The network ID of Subnet1 and subnet2 are both B type address with 23bits network ID length
  - $PC_a$ and $PC_b$ work as DHCP client, Router work as DHCP server
  - On the Router, there are three ip-pool with different netwok and different gateway-list
+ Check
  - The ip address of $PC_a$ and $PC_b$
  - using cmd "ping” to test the connection between to PCs, are they reachable or not? Why?

### Option practice （use two routers）
1. Implement cross-router communication
2. Show the rout-table and fib info on $Router_A$ and $Router_B$
3. Save the configuration as setup configuration

<div>
  <img src="./pngs/lab12_pracrtice_03_01.png"><br />
  <div>1st</div>
</div>

### Tips

+ Tips : reboot
<div>
  <img src="./pngs/lab12_pracrtice_04_01.png"><br />
  <div>1st</div>
</div>

In user view "reboot” will reminds to save the current configuration as startup cfg, if you choose yes , the configuration will work on the coming reboot stage.

+ Tips(make USB Serial Port work)：
Plug the USB-to-RT45 console port in USB port on PC, if the ‘USB Serial Port' couldn't be found in the ‘COM and LPT' of Device Manager, it means stalling the driver is needed. Open the Device Manger, then following the steps:
<div>
  <img src="./pngs/lab12_pracrtice_04_02.png"><br />
  <div>2nd</div>
</div>

<div>
  <img src="./pngs/lab12_pracrtice_04_03.png"><br />
  <div>3rd</div>
</div>

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