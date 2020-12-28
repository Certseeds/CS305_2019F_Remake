<!--
 * @Github: https://github.com/Certseeds/CS305_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-08-01 15:46:53
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-01 15:55:21
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->

## Report 10 Details

### Question 1

1. Initiates an ICMP session to test if [www.example.com](www.example.com) is reachable(setting the packet size is 3200B ), capture the packets.

+ How to initiates an ICMP Echo request with 3200B length?
+ Is there any fragmentation on the IP packets , how do you find it ?
+ How many fragments of a 3200B length IP packet ?
+ How do you identify the ICMP Echo request and Echo reply?
+ For the ICMP Echo request, which fragment is the 1st one, which is the last ? How do you identify them?
+ What's the length of each IP fragment? Is the sum of each fragment's length equal to the original IP packet ? 
+ Please add the necessary screenshots and calculation when answering questions. 

### Question 2

using tracert (windows) / traceroute(linux or MacOS) to trace the route from your host to  [www.sustech.edu.cn](www.sustech.edu.cn) capture the packets while tracing

+ Is there any "Time-to-live exceeded" ICMP packets?
+ what's the difference between these packets and normal ICMP packets(such as ICMP echo request)? List at least 3 aspects.
+ Please add the necessary screenshots when answering questions. 

### Question 3

Initiates a DHCP session

+ How to initiate a DHCP session? How to find the DHCP session packets?
+ What 's the source IP address and destination IP address of a DHCP request? What is the type of these two IP address?
+ What info items are required for a host if it need to contact with others in the Internet?
+ How do you find the Lease Time of a dynamic IP address? What's the value of it? In which type of DHCP packet could this field be set? 
+ Please add the necessary screenshots when answering questions. 

