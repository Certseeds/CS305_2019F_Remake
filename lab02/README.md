<!--
 * @Github: https://github.com/Certseeds/CS305_Remak
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 18:25:49
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-08 22:50:47
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 02 Details
1. 
    + filename: prime.py
    + requirement:
    implement a function to find prime in a range
    function signature:
    `def find_prime(start: int, end: int) -> List[int]`

2. Use Wireshark to capture packets and answer the questions with your screenshots:
    + Open http://example.com in your browser, what kind of display filter do you need to filter out HTTP packets?
  
    + How many layers do you see in the HTTP request packet? What's the src ip addr, src port, dst ip addr and dst port of the request pack?t?
  
    + What kind of information can be found in the HTTP response packet? Is there anything same with the information which is displayed on your browser?

3. Use Wireshark to capture packets and answer those questions with your screenshots (both Wireshark and tracert display):
    + Using a proper capture filter/display filter to capture/display a tracert traffic. And start tracert baidu.com.
  
    + How many packets did tracert send for each hop?
  
    + How many kinds of response did tracert receive from the remote? What's the source IP address of these response messa?e?
  
    + Try to calculate the RTT (round-trip time) between your host and baidu.com based on your capture instead of tracert display. Are they same with tracert display?