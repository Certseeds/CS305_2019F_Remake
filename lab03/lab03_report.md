<!--
 * @Github: https://github.com/Certseeds/CS305_Remak
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-19 16:06:56
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-08-08 22:51:15
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## <div>CS305 Computer Network</div>
## <div>Report_Lab03</div>

**SID**:  $********$  
**Name**:  nanoseeds  


### Question 1

1. Using cURL make Get request to http://httpbin.org/request  
The command is:
`curl -GET -v http://httpbin.org/get`

``` log
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 34.235.192.52...
* TCP_NODELAY set

  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0* Connected to httpbin.org (34.235.192.52) port 80 (#0)

  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0> GET /get HTTP/1.1
> Host: httpbin.org
> User-Agent: curl/7.58.0
> Accept: */*
> 
< HTTP/1.1 200 OK
< Date: Fri, 19 Jun 2020 13:21:52 GMT
< Content-Type: application/json
< Content-Length: 254
< Connection: keep-alive
< Server: gunicorn/19.9.0
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
< 
{ [254 bytes data]

100   254  100   254    0     0    116      0  0:00:02  0:00:02 --:--:--   116
* Connection #0 to host httpbin.org left intact
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/7.58.0", 
    "X-Amzn-Trace-Id": "Root=1-5eecbbf0-3ca0c680914ed06f98a4c887"
  }, 
  "origin": "111.222.16.85", 
  "url": "http://httpbin.org/get"
}
```

2. In this log, I get the request head and response head & response body – a json file. 
For request,

+ 1st line means Host: the aimed domain address of web is httpbin.org
+ 2nd line means the User-Agent it use is "cURL/7.66.0"
+ 3rd line means the Accept is just "*/*" (maybe means accept anything)

3. For response,

+ 1st, it uses HTTP1.1 protocol and the status code are 200, which means OK.
+ 2nd, Date is the server's date when its response this packet.
+ 3rd, The Media type of the body of the request (used with POST and PUT requests).
+ 4th, The length of the response body in octets (8-bit bytes)
+ 5th, Control options for the current connection and list of hop-by-hop request fields.
+ 6th, A name for the server. in this case, it's gunicorn/19.9.0.
+ 7th, Specifying which web sites can participate in cross-origin resource sharing.
+ 8th, same as 7th.

4. wireshark screenshot

<div>
  <img src=" ./pca_pngs/lab03_01_01.png"><br />
  <div>Fig.1</div>
</div>

<div>
  <img src=" ./pca_pngs/lab03_01_02.png"><br />
  <div>Fig.2</div>
</div>

<div>
  <img src=" ./pca_pngs/lab03_01_03.png"><br />
  <div>Fig.3</div>
</div>

this part, analysis is same as directly curl

### Question 2

1. Using cURL make Get request to http://httpbin.org/request  
The command is:
`curl -d "username=foo&password=bar" POST http://httpbin.org/post`

``` log
* Rebuilt URL to: POST/
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0* Could not resolve host: POST
* Closing connection 0
curl: (6) Could not resolve host: POST

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 34.235.192.52...
* TCP_NODELAY set
* Connected to httpbin.org (34.235.192.52) port 80 (#1)
> POST /post HTTP/1.1
> Host: httpbin.org
> User-Agent: curl/7.58.0
> Accept: */*
> Content-Length: 25
> Content-Type: application/x-www-form-urlencoded
> 
} [25 bytes data]
* upload completely sent off: 25 out of 25 bytes
< HTTP/1.1 200 OK
< Date: Fri, 19 Jun 2020 13:43:38 GMT
< Content-Type: application/json
< Content-Length: 454
< Connection: keep-alive
< Server: gunicorn/19.9.0
< Access-Control-Allow-Origin: *
< Access-Control-Allow-Credentials: true
< 
{ [454 bytes data]

100   479  100   454  100    25    543     29 --:--:-- --:--:-- --:--:--   572
100   479  100   454  100    25    542     29 --:--:-- --:--:-- --:--:--   572
* Connection #1 to host httpbin.org left intact
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "password": "bar", 
    "username": "foo"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Content-Length": "25", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/7.58.0", 
    "X-Amzn-Trace-Id": "Root=1-5eecc10a-c5d24d1896e9e4ad71cfc8c8"
  }, 
  "json": null, 
  "origin": "111.222.16.85", 
  "url": "http://httpbin.org/post"
}
``` 
Using cURL receive a json file in the end, and in this process, of course the request and reponse's head message will be get.

2. For request,

+ 1 st line means it's a POST packets use HTTP1.1 protocol and request url is /post for host.
+ 2 nd line means Host: the aimed domain address of web is httpbin.org
+ 3 rd line means the User-Agent it use is "curl/7.58.0"
+ 4 th line means the Accept is just "*/*" (maybe means accept anything)
+ 5 th line means the length of the post message is 25 bytes.
+ 6 th lines means the type of post message is "application/x-www-form—urlencoded" Which means "HTML form submission"

3. For response 

+ 1st, it uses HTTP1.1 protocol and the status code are 200, which means OK.
+ 2nd, Date is the server's date when its response this packet.
+ 3rd, The Media type of the body of the request (used with POST and PUT requests).
+ 4th, The length of the response body in octets (8-bit bytes)
+ 5th, Control options for the current connection and list of hop-by-hop request fields.
+ 6th, A name for the server. in this case, it's gunicorn/19.9.0.
+ 7th, Specifying which web sites can participate in cross-origin resource sharing.
+ 8th, same as 7th.

4. 

<div>
  <img src=" ./pca_pngs/lab03_02_01.png"><br />
  <div>Fig.4</div>
</div>

<div>
  <img src=" ./pca_pngs/lab03_02_02.png"><br />
  <div>Fig.5</div>
</div>

<div>
  <img src=" ./pca_pngs/lab03_02_03.png"><br />
  <div>Fig.6</div>
</div>
Also same as directly run curl.

##### In conclusion, the packet captured by Wireshark is capture correspond to the cURL request.

<style type="text/css">
div{
  text-align: center;
}
div>div {
  text-align: center;
  border-bottom: 1px solid #d9d9d9;
  display: inline-block;
  padding: 2px;
}
div>img{
  border-radius: 0.3125em;
  box-shadow: 0 2px 4px 0 rgba(34,36,38,.12),0 2px 10px 0 rgba(34,36,38,.08);
}
</style>