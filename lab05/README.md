<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-22 22:12:33
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-06-23 09:39:36
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 05 Details

### before introduce
+ Please finish the lab according to this file
  + submit the report of lab 5 based on the lab report template.
  + submit your source code in zip file.
    + comments is MUST
    + DO NOT copy paste any existing source code of DNS resolver

### Task 1
+ make an DNS query which will invoke the EDNS0
  + Screenshot on this command and its output

+ capture the packages using Wireshark
  + what is the content of this query message
    + Find the name, type and class of this query
    + How can you tell this DNS query is based on EDNS0
    + From this query massage , can it handle DNSSEC security RRs or not
  + what is the content of this response message
    + Is there any answers, what's the ttl of each answer
    + Is there any authority RRs, what's the type of each RR
    + Is there any special additional RRs with OPT type, what does its 'Do bit' say: Does it accept DNSSEC security RRs or not

### Task 2
+ Make the query by using query method of “dns resolver”(a python package)
  + To query the type A value of www.sina.com.cn based on TCP and UDP stream respectively

+ capture the related TCP stream and UDP stream using Wireshark
  + Screenshot on this two commands .
  + what’s the default transport lay protocol while invoke DNS query
  + Screenshot on the TCP stream of query by TCP. how many TCP packets are captured in this stream, Which port is used?
  + Screenshot on the UDP stream of query by UDP. how many UDP packets are captured in this stream, Which port is used?
  + Is there any difference on DNS query and response message while using TCP and UDP respectively

### Task 3 : implement a local resolver
+ Function:
   + Listen and accept DNS queries.
    + Support common query types:
    A, AAAA, CNAME, TXT, NS, MX
    + EDNS implementation is not required.
  + Forward query to a upstream DNS resolver (or a public DNS server).
  + Check out the response and send response to your clients.
  + Maintain a cache of DNS query-response of all results.
+ Test method:
  + using dig sending query to your resolver
+  <font color="red">**comments is MUST**</font>
+ <font color="red">**DO NOT copy paste any existing source code of DNS resolver**</font>

### Tips for Task 2
query in dns.resolver of python
+ query(self, qname, rdtype=1, rdclass=1, tcp=False, source=None, raise_on_no_answer=True, source_port=0)
  + Query nameservers to find the answer to the question.
  + The qname, rdtype, and rdclass parameters may be objects of the appropriate type, or strings that can be converted into objects of the appropriate type. E.g. For rdtype the integer 2 and the the string 'NS' both mean to query for records with DNS rdata type NS.

+ Parameters:
  + qname (dns.name.Name object or string) - the query name
  + rdtype (int or string) - the query type
  + rdclass (int or string) - the query class
  + tcp (bool) - use TCP to make the query (default is False).
  + source (IP address in dotted quad notation) - bind to this IP address (defaults to machine default IP).
  + raise_on_no_answer (bool) - raise NoAnswer if there's no answer (defaults is True).
  +  source_port (int) - The port from which to send the message. The default is 0.

### Tips for Task 3
1. udp_c.py

``` python 
from socket import *

serverName: str = '127.0.0.1'
serverPort: int = 12000
clientSocket: socket = socket(AF_INET, SOCK_DGRAM)
message: str = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```

2. udp_s.py

``` python
from socket import *

serverPort: int = 12000
serverSocket: socket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage: str = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

```