<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 16:06:56
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-06-20 12:17:12
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## <div>CS305 Computer Network</div>
## <div>HW2_Report</div>

**SID**:  \*\*\*\*\*\*\*\*   
**Name**:  nanoseeds  

### Question 1
1.	A transport protocol can provide can provide: 
  + "data integrity"
  + "timing"
  + "throughput" 
  + "security" 
four broad classes of services.

2. shou in table
	
|    service     |                                 TCP                                  |          UDP           |
| :------------: | :------------------------------------------------------------------: | :--------------------: |
| data integrity |                               support                                |   can’t provide this   |
|     timing     |                         cannot provide this                          | do not support it too. |
|   throughput   |                          don’t provide this                          |  don’t provide it too  |
|    security    | don’t provide this originally,but can use SSL to easily provide that |   don’t provide it.    |


### Question 2
First of all, Usually DNS lookup use UDP protocol, so the DNS step cost const time whether choose which TCP or HTTP choice, it always be $\sum_{i=1}^{n}{RTT_i}$.
1. If the HTTP is Non-persistent with no parallel TCP connections Then, it should take 9 times “three times handshake and object get”, which cost $9 *(RTT_0 *2) = 18RTT_0$

2. If Non-persistent HTTP with the browser configured for 5 parallel connections:
  Then the browser needs to get the html file first, it cost $2RTT_0$.
  Then, the other objects need $⌈8/5⌉*2RTT_0 = 4RTT_0$.
  So, it needs $6RTT_0$ to transfer the web
	
3. Persistent HTTP, it cost $1 RTT_0$ to build the TCP connection. And cost $9*1RTT_0$ to transfer 9 objects. After ALL, it cost $10RTT_0$.
	
4. In conclusion, 
  + the HTTP is Non-persistent with no parallel TCP connections cost  $\sum_{i=1}^{n}{RTT_i} + 18RTT_0$
  + Non-persistent HTTP with the browser configured for 5 parallel connections cost  $\sum_{i=1}^{n}{RTT_i}  + 6RTT_0$
  + Only Persistent HTTP cost $\sum_{i=1}^{n}{RTT_i}  + 10RTT_0$


### Question 3
0. First, us is server upload capacity & dmin is min client download rate

1.	
  + Because the goal of distribution scheme is set time to $NF/u_s$, so we just set for every client, the download speed is $u_s/N$, where N is the client number.  
  their speed is the same $u_s/N$, so they will finish at the same time, which cost is $F/(u_s/N) = NF/u_s$.
  + 在$u_s/N <= d_{min}$的时候,在这种情况下,先以平均速率向每个client传输,因为已经到达server的最高速率,所以增加任何一个的速率都会减少另外一方的速率,所以最快的方式是以平均速率向每个cilent和传输,耗时为$F/(u_s/N)$ = $FN/u_s$.(时间被服务器带宽所约束).

2.	In this case $u_s/N> d_{min}$, the server just set the speed of every client is $d_min$, the sum of speed is still $N*d_{min}<u_s$ (which means it can be done), so every client will cost the same time, which is $F/d_{min}$.(时间被最慢下载者的带宽所约束).

3.	In conclusion, 
  + if $u_s/N<d_{min}$, the distribution time can be $NF/u_s$ but cannot be $F/d_{min}$ because the us is too small, can not suppose the speed that bigger than $u_s/N$.  
  + If $u_s/N>= d_{min}$, the distribution time can be $F/d_{min}$ and the client’s speed cannot suppose the server’s max speed so time cannot be $NF/u_s$.    
  + In these two cases, first use all of the server’s speed, the second use all of the minimum speed of client’s max-download rate. Each kind of wat can not improve. 

In conclusion, minimum distribution time is in general given by max $(NF/u_s, F/ d_{min})$.


### Question 4
0. 首先我们来讨论题目内的符号的含义.
  + $u_s$:server最大上传带宽.
  + $u_i$:第i个client的上传带宽
  + 定义 $u = (\sum_{i=1}^{n}{u_i})$  
1. 
  + If $u_s <= (u+u_s)/N$ , then while the server sends bits to every client, the client also sends what It get to other clients, which use its upload rate to do that. But all bits come from the server, the server should send one complete copy. Which cost $F/u_s$, and while the server sends the bits, clients exchange bits to each other, so when server send one complete copy, the clients all get a copy. while this process, the server’s rate distribution is decided by the client’s upload rate, the upload rate quicker, the download rate quicker it get; what’s more, it should send bits to every client to make full use of their upload rate.
  + $u_s <= (u+u_s)/N$, 
  所以 $u_s <= (u_s+u)/N$ ===> $(N-1)u_s <= u$ (Equation 1).  
  首先,Server端按照每个client上传的带宽分配下载带宽$r_i=(u_i/u)*u_s$,然后,每个client都会向其他的client上传,速率为${r_i} * (N-1) =(u_i/u) * u_s * (N-1) <= u_i * (u/u)=u_i$,也就是说每个client的上传速率都还不满$u_i$.因此,对于每个client,都可以及时的下载到server端的上传.限制因素为$u_s$.
  由Equaltion1 可得,$F/u_s<NF/(u_s+u)$.

2. 
  + If $u_s>= (u+u_s)/N$ , then while the server sends bits to every client, the clients cannot send all received bits, so after the server send one complete copy, clients can not all get one complete copy.
  So, we think them as one complete system. In this system the upload rate is $u+u_s$ and have a complete copy. It should upload N*F to make sure every client gets one copy. So, the server provides the rate of every client that is direct ratio to their upload rate.it need cost $NF/u$.  
	+ 在这种情况下,$u_s>= (u+u_s)/N$, 
  所以 $u_s>= (u_s+u)/N$ ====> $(N-1)u_s>= u$ (Equation 2).  
  首先,Server端按照每个client上传的带宽分配下载带宽$r_i=u_i/(N-1)$, 这里注意,$\sum_{i=1}^{n}{r_i}=u/(N-1)<=u_s$  
  服务器端还有剩下的带宽.将剩下的带宽$(u_s)-u/(N-1)$平均分配给每一个client,所以每个$client_i$的带宽$r_{n+1}$实际上为$r_i+(u_s-u/(N-1))/N$
  每个Client所接受的带宽为$r_i+r_{n+1}+\sum_{j!=i}^{n}{r_j}=(u_s+u)/N$
  因此,每个client的下载时间都为$FN/(u_s+u)$.
3. 
  + If $F/u_s>=(u+u_s)/N$, the system need $F/u_s$ time to transfer the file; 
  + if $F/u_s <= ((u+u_s)/N)$ , it need $NF/(u+u_s)$ time. 
  + And each choice gets its best. At least the server should send one copy and each client should get one copy.

4. In conclusion, the minimum distribution time is in general given by max $(F/u_s, NF/(u+u_s))$.


### Question 5
1. Because of every video version have possibility connect with every audio version, there will be $N^2$ files.
2. In the other hand, if video and audio is divide, the serve only need $2*N$ files (N video version, N audio version)
