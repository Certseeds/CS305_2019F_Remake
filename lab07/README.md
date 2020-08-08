<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-28 21:13:35
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-01 15:54:57
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 07 Details

### Question 1 : Select one UDP packet from your trace. From this packet,
determine

1. how many fields there are in the UDP header.

2. the name of each fields in the UDP header.

3. the length (in bytes) of each fields in the UDP header.

4. What is the maximum number of bytes that can be included in a UDP payload? (Hint: the answer to this question can be determined by your answer to 3) above)

5. What is the largest possible source port number? (Hint: same as the hint in 4) above.)

6. What is the protocol number for UDP?( Give your answer in both hexadecimal and decimal notation.) 

### Question 2
Finish the question 4，6，7，9，10，12.

4. What is the sequence number of the TCP SYN segment that is used to initiate the TCP connection between the client computer and gaia.cs.umass.edu? What is it in the segment that identifies the segment as a SYN segment?

5. What is the sequence number of the SYNACK segment sent by gaia.cs.umass.edu to the client computer in reply to the SYN? What is the value of the Acknowledgement field in the SYNACK segment? How did gaia.cs.umass.edu determine that value? What is it in the segment that identifies the segment as a SYNACK segment?

6. What is the sequence number of the TCP segment containing the HTTP POST command? Note that in order to find the POST command, you’ll need to dig into the packet content field at the bottom of the Wireshark window, looking for a segment with a “POST” within its DATA field.

7. Consider the TCP segment containing the HTTP POST as the first segment in the TCP connection. What are the sequence numbers of the first six segments in the  TCP connection (including the segment containing the HTTP POST)? At what time was each segment sent? When was the ACK for each segment received? Given the difference between when each TCP segment was sent, and when its acknowledgement was received, what is the RTT value for each of the six segments? What is the EstimatedRTT value (see Section 3.5.3, page 242 in text) after the receipt of each ACK? Assume that the value of the EstimatedRTT is equal to the measured RTT for the first segment, and then is computed using the EstimatedRTT equation on page 242 for all subsequent segments.
  Note: Wireshark has a nice feature that allows you to plot the RTT for each of the TCP segments sent. Select a TCP segment in the “listing of captured packets” window that is being sent from the client to the gaia.cs.umass.edu server. Then select: Statistics->TCP Stream Graph->Round Trip Time Graph.

8. What is the length of each of the first six TCP ${segments?}^4$

9. What is the minimum amount of available buffer space advertised at the received for the entire trace? Does the lack of receiver buffer space ever throttle the sender?

10. Are there any retransmitted segments in the trace file? What did you check for (in the trace) in order to answer this question?

11. How much data does the receiver typically acknowledge in an ACK? Can you identify cases where the receiver is ACKing every other received segment (see Table 3.2 on page 250 in the text).

12. What is the throughput (bytes transferred per unit time) for the TCP connection? Explain how you calculated this value.

### Question 3
In this assignment, you need to implements a RDT protocol on UDP socket.
1. Requirement
    1. Your protocol needs to ensure the reliability of data transfer. Packet loss and payload corruption might happen.
        + To deal with packet loss, using ack and retransmission according to GBN the textbook.
        + To deal with payload corruption, you need to design a checksum of your payload.
    2. Your RDT protocol should be like TCP, which means it’s a stream-oriented protocol, not packet-oriented.
        +  To establish a connection, you might need to do things like things in TCP:
            1. SYN
            2. SYN, ACK
            3. ACK
        + . To close a connection, you might need to do things like things in TCP:
            1. FIN
            2. ACK
            3. FIN
            4. ACK
    3. Payload : 
        Your payload might be like this:

| SYN   | FIN   | ACK   | SEQ    | SEQ ACK | LEN    | CHEKCSUM | Payload |
| :---- | :---- | :---- | :----- | :------ | :----- | :------- | :------ |
| 1 bit | 1 bit | 1 bit | 4 byte | 4 byte  | 4 byte | 2 byte   | LEN     |

> Checksum Calculation Example(just for reference)
``` python
def calc_checksum(payload: bytes) ->int:
    sum:int = 0
    for byte in payload:
        sum += byte
    sum = -(sum % 256)
    return (sum & 0xFF)
```

2. API reference:

+ rdt code example:

``` python
from udp_socket import UDPsocket # import provided class
class socket(UDPsocket):
    def __init__():
        super(socket, self).__init__()
    # send syn; receive syn, ack; send ack
    def connect():
        # your code here
        pass
    
    # receive syn; send syn, ack; receive ack
    def accept():
        # your code here
        pass
    
    # send fin; receive ack; receive fin; send ack
    def close():
        # your code here
        pass
    
    def recv():
        # your code here
        pass
    
    def send():
        # your code here
        pass
``` 

+ server code example:

``` python
from rdt_socket import rdt_socket
server = rdt_socket()
server.bind((SERVER_ADDR, SERVER_PORT))
# SERVER_ADDR : str like '127.0.0.01'
# SERVER_PORT : int random.randint(1,65535)
while True:
    conn, client = server.accept()
        while True:  
            data = conn.recv(2048)
            if not data: break
                conn.send(data)
            conn.close()
```

+ client code example:

``` python
from rdt import socket
client = socket()
client.connect((SERVER_ADDR, SERVER_PORT))
# SERVER_ADDR : str like '127.0.0.01'
# SERVER_PORT : int random.randint(1,65535)
client.send(MESSAGE)
data = client.recv(BUFFER_SIZE)
assert data == MESSAGE
client.close()
```