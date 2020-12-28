<!--
 * @Github: https://github.com/Certseeds/CS305_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 22:02:07
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-06-20 10:10:36
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->

## <div>CS305 Computer Network</div>
## <div>Report_HW1</div>

**SID**:  $********$  
**Name**:  nanoseeds  


### Question 1

1.	The packet switch's packets" length is p bits, so the message has ⌈x/p⌉ packets,

First of all, in the question nodal processing delay and queue delay can be neglected. For one packet, it's one-step transmission delay is p/b second, the propagation delay is d second. Because there are k links, so for one packet, the sum time is (p/b + d) $*$ k. we just consider when the last packets arrive to the other way, the last packets was begin to send in (p/b)$*$( ⌈x/p⌉-1), itself take (p/b + d)$*$k.

So, packet switch takes (p/b) $*$(k+⌈x/p⌉-1) +k$*$d

2.	Circuit switch:
First, create a circuit should costs second. They x bits need x/d bits to send in the network, between it cost d second, all the time is (s + x/d +k*d)
So, if (p/b) $*$(k+⌈x/p⌉-1) +k $*$ d < (s + x/d +k$*$d)
 (p/b) $*$(k+⌈x/p⌉-1) < s + x/d

3.	Inclusion if (p/b) $*$(k+⌈x/p⌉-1) < s + x/d, then the delay of packet switch is smaller than that of the circuit switch.


### Question 2

1. First of all, handshaking process cost 2RTT = 200ms.  
Then,1KB = 8Kb, because the packets can be continuously transmitted.  
So 1000KB = 8000Kb= 8000 $*$ 1024 bits, the transmission bandwidth = $1.5*10^6$ bits/s,
$8000*1024/(1.5*10^6) = (5+173/375)s ≈ 5461.33ms$  
So, this file need 5408.33ms to transmitted

2. First of all, handshaking process cost 2RTT, which is 200ms
If its meaning is when one packet is transmitted, then the other side will cost RTT to send a receiver.  
So, the all steps equal one half RTT+(transmit a packet + RTT) $*$ 1000  
One half RTT is 150ms  
Transmit a packet is $8*1024 bits/ (1.5*10^6 bits/s) = (5+173/375) ms = 5.46133 ms$
So this file need $150 +(5+173/375+100)*1000 ≈ 105611.33ms$  
However, we should consider the final receiver is useless, which cost 50ms
So, this file cost 105611.33 ms

3. First of all, it cost 2RTT, which is 200ms.

Then file transmission delay is 0, so in first 2RTT,20packets can be transmitted.  
It still needs (1000-20) = 980 packets, after every 1RTT 20 packets can be transmitted, so it cost 980/20*100ms = 4900ms  
This file cost 5100ms.  

### Question 3

|                       access technologies                        |          Type           |
| :--------------------------------------------------------------: | :---------------------: |
|            Digital Subscriber Line using twisted pair            |       Home Access       |
|            Cable Internet Access using coaxial cable             |       Home Access       |
|            Fiber to The Home using fiber optic cable             |       Home Access       |
| Ethernet(usually use twisted pair to connect with router/switch) |    Enterprise Access    |
|                           Wireless LAN                           |    Enterprise Access    |
|                           3G/4G/5G/LTE                           | Wide-area mobile Access |



### Question 4
1. 
+ Email (like Foxmail)-SMTP/POP3/IMAP,
+ Web Brower (Chrome or Firefox) use HTTP or HTTPS protocols 
+ file downloader (such as IDM) use FTP protocol 
+ DNS use DNS protocols
+ P2P applications (like BitComet) use BitTorrent protocol (one kind of P2P protocol)
+ Internet phone (like skype) use SIP/RTP.

1. First of all, this process needs another host's ip address, then it needs the other process's port number.
