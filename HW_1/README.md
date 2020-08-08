<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 21:58:33
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-06-20 10:13:32
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Homework #1
1. Compare packet switch and circuit switch under the following scenario. Suppose you would like to deliver a message of x bit. There are k links from the source to destination. The propagation delay of each link is d second, the transmission rate is b bit/second. The circuit setup time under circuit switch is s second. Under packet switch network, when the packet length is p bit, the queue delay in every node can be neglected. Please calculate the condition, under which the delay of packet switch is smaller than that of the circuit switch.

2. Calculate the overall delay of transmitting a 1000KB file under the following circumstance. The overall delay is defined as the time from the starting point of the transmission until the arrival of the last bit to the destination. RTT is assumed to be 100ms, one packet is 1KB (1024B) size. The handshaking process costs 2RTT before transmitting the file.
  +  Transmission bandwidth is 1.5Mb/s, the packets can be continuously transmitted.
  + Transmission bandwidth is 1.5Mb/s, but when one packet is transmitted, the next packet should wait for 1 RTT (waiting for the acknowledgement of the receiver) before being transmitted.
  + Transmission bandwidth is infinite, i.e. transmission delay is 0. After every 1 RTT, as many as 20 packets can be transmitted.

3. List six access technologies. Classify each of them as home access, enterprise access, or wide-area mobile access.

4. 
  + List five nonproprietary Internet applications and the application-layer protocols that they use.
  + What information is used by a process running on one host to identify a process running on another host? 