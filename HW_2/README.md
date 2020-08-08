<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-20 09:24:12
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-06-20 10:28:10
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## CS305 Computer Network
## Homework 2
1. List the four broad classes of services that a transport protocol can provide. For each of the service classes, indicate if either UDP or TCP (or both) provides such a service.

2. Suppose within your Web browser you click on a link to obtain a Web page. The IPaddress for the associated URL is not cached in your local host, so a DNS lookup is necessary to obtain the IP address. Suppose that n DNS servers are visited before your host receives the IP address from DNS; the successive visits incur an RTT of $RTT_1, . . ., RTT_n$.
Further suppose that the Web page associated with one HTML file, and the HTML filereferences eight very small objects on the same server. Let RTT0 denote the RTT between the local host and the server containing these objects. Assuming zero transmission time of the objects. Please calculate the time which elapses from when the client clicks on the link until the client receives the object under the following circumstance.
  +  Non-persistent HTTP with no parallel TCP connections?
  +  Non-persistent HTTP with the browser configured for 5 parallel connections?
  +  Persistent HTTP?

3. Consider distributing a file of F bits to N peers using a client-server architecture. Assume a fluid model where the server can simultaneously transmit to multiple peers, transmitting to each peer at different rates, as long as the combined rate does not exceed us.
  + Suppose that $u_s/N ≤ d_{min}$. Specify a distribution scheme that has a distribution time of $NF/u_s$.
  + Suppose that $u_s/N ≥ d_{min}$. Specify a distribution scheme that has a distribution time of $F/d_{min}$.
  + Conclude that the minimum distribution time is in general given by max $({NF/u_s, F/ d_{min}})$.

4. Consider distributing a file of F bits to N peers using a P2P architecture. Assume a fluid
model. For simplicity assume that dmin is very large, so that peer download bandwidth is
never a bottleneck.
  + Suppose that $u_s ≤ (u_s + u_1 + ... + u_N)/N$. Specify a distribution scheme that has a distribution time of $F/u_s$.
  + Suppose that $u_s ≥ (u_s + u_1 + ... + u_N)/N$. Specify a distribution scheme that has a distribution time of $NF/(u_s + u_1 + ... + u_N)$. 
  + Conclude that the minimum distribution time is in general given by max $({F/u_s, NF/(u_s + u_1 + ... + u_N)})$.
  
5. Consider a DASH system for which there are N video versions (at N different rates and q0ualities) and N audio versions (at N different rates and qualities). Suppose we want to allow the player to choose at any time any of the N video versions and any of the N audio versions.
  + If we create files so that the audio is mixed in with the video, so server sends only one media stream at given time, how many files will the server need to store (each a different URL)?
  + If the server instead sends the audio and video streams separately and has the client synchronize the streams, how many files will the server need to store?