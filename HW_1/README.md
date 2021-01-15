<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 22:02:07
 * @LastEditors: nanoseeds
 * @LastEditTime: 2021-01-15 11:24:14
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->

# <div>CS305 Computer Network</div>

# <div>Report_HW1</div>

**SID**:  $********$  
**Name**:  nanoseeds  

## Question 1

Compare packet switch and circuit switch under the following scenario Suppose you would like to deliver a message of $x$ bit.There are $k$ links from the source to destination.The propagation delay of each link is $d$ second,the transmission rate is $b$ bit/second.The circuit set up time under circuit switch is $s$ second.Under packet switch network,when the packet length is $p$ bit,the queue delay in every node can be neglected.Please calculate the condition,under which the delay of packet switch is smaller than that of the circuit switch.

1. The packet switch's packets' length is $p$ bits, so the message has $⌈\frac{x}{p}⌉$ packets,

First of all, in the question nodal processing delay and queue delay can be neglected. For one packet, it's one-step transmission delay is $\frac{p}{b}$ second, the propagation delay is d second. Because there are k links, so for one packet, the sum time is $(\frac{p}{b} + d) * k$

we just consider when the last packets arrive to the other way, the last packets was begin to send in $\frac{p}{b}*(⌈\frac{x}{p}⌉-1)$, itself take $(\frac{p}{b} + d)*k$.

So, packet switch takes $\frac{p}{b} *(k-1+⌈\frac{x}{p}⌉) +k*d$

2. Circuit switch:
First, create a circuit should costs second. They $x$ bits need $\frac{x}{b}$ bits to send in the network, between it cost $d$ second, all the time is $s + \frac{x}{b} +k*d$

So, if $\frac{p}{b} *(k-1+⌈\frac{x}{p}⌉)+k*d < (s + \frac{x}{b} +k*d)$

we support $x$ can be divided by $p$.

3. Inclusion if $p < \frac{sb}{k-1}$, then the delay of packet switch is smaller than that of the circuit switch.

## Question 2

Calculate the over all delay of transmitting a 1000KB file under the following circumstance.The over all delay is defined as the time from the starting point of the transmission until the arrival of the last bit to the destination. RTT is assumed to be 100 ms,one packet is 1KB(1024B) size.The hand shaking process costs 2RTT before transmitting the file.

+ Transmission band width is 1.5Mb/s,the packets can be continuously transmitted.
+ Transmission band width is1.5Mb/s,but when one packet is transmitted then ext packet should wait for 1RTT(waiting for the acknowledgement of the receiver)before being transmitted.
+ Transmission band width is infinite, i.e.transmissiondelay is 0.After every 1RTT,asmany as 20packets can be transmitted.

1. First of all, handshaking process cost 2RTT = 200ms.  
Then,1KB = 8Kb, because the packets can be continuously transmitted.  
So 1000KB = 8000Kb, the transmission bandwidth = $1500Kb/s$,
$8000/1500 = 16/3s ≈ 5333ms$  
Do not forget the half RTT to transfer packet to other side.
so $\frac{16}{3}+100*2.5=5.583s$
So, this file need 5.583s to transmitted

2. First of all, handshaking process cost 2RTT, which is 200ms
compare to First, waiting time is more than 999 RTT, so time is 
$5.583+999*0.1=105.483s$

3. First of all, it cost 2RTT, which is 200ms. the transpose time is half RTT, which is 50ms.

Then file transmission delay is 0, so in first 2RTT,20packets can be transmitted.  
It still needs (1000-20) = 980 packets, after every 1RTT 20 packets can be transmitted, so it cost 980/20*100ms = 4900ms  
This file cost 5150ms.  

## Question 3

List six access technologies. Classify each of them as home access,enterprise access,or wide-area mobile access.

|                       access technologies                        |          Type           |
| :--------------------------------------------------------------: | :---------------------: |
|            Digital Subscriber Line using twisted pair            |       Home Access       |
|            Cable Internet Access using coaxial cable             |       Home Access       |
|            Fiber to The Home using fiber optic cable             |       Home Access       |
| Ethernet(usually use twisted pair to connect with router/switch) |    Enterprise Access    |
|                           Wireless LAN                           |    Enterprise Access    |
|                           3G/4G/5G/LTE                           | Wide-area mobile Access |

## Question 4

1. List five non proprietary Internet application sand the application-layer protocols that the yuse.

+ Email (like Foxmail)-SMTP/POP3/IMAP.
+ Web Brower (Chrome or Firefox) use HTTP or HTTPS protocols
+ file downloader (such as IDM) use FTP protocol
+ DNS use DNS protocols
+ P2P applications (like BitComet) use BitTorrent protocol (one kind of P2P protocol)
+ Internet phone (like skype) use SIP/RTP.
+ remote terminal access: Telnet

2. What information is used by aprocess running on one host to identify aprocess running on another host?

+ First of all, this process needs another host's ip address, then it needs the other process's port number.
