<!--
 * @Github: https://github.com/Certseeds/CS305_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-08-01 15:41:28
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-01 15:55:07
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 08 Details

### Practice( do not need report)

+ start up Wireshark and begin packet capture (Capture->Start) and then press OK on the Wireshark Packet Capture Options screen
+ Go the http://gaia.cs.umass.edu/wiresharklabs/alice.txt and retrieve an ASCII copy of Alice in Wonderland
+ Stop Wireshark packet capture.
  + Analysis the tcp stream
  + Any duplicate ack
  + Any tcp segment with sack option
  + Any tcp retransmission? Is it retransmission or fast retransmission
  + Any window size 0 , what happened next
  + Find the tcptrace view of this tcp session, what's the relationship of two curve
