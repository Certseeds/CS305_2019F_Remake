<!--
 * @Github: https://github.com/Certseeds/CS305_2019F_Remake
 * @Organization: SUSTech
 * @Author: nanoseeds
 * @Date: 2020-06-20 12:24:03
 * @LastEditors: nanoseeds
 * @LastEditTime: 2020-06-20 12:49:11
 * @License: CC-BY-NC-SA_V4_0 or any later version 
 -->
## Report 04 Details
1. Using asyncio to implement an Echo Server with the same function as Example: `Echo Server`.

``` python
import socket

def echo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 5555))
    sock.listen(10)
    while True:
        conn, address = sock.accept()
        while True:
            data = conn.recv(2048)
            if data and data != b'exit\r\n':
                conn.send(data)
                print(data)
            else:
                conn.close()
                break

if __name__ == "__main__":
    try:
        echo()
    except KeyboardInterrupt:
        exit()
```
References: `Echo Server Multithreading Example`

``` python
class Echo(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address

    def run(self):
        while True:
            data = self.conn.recv(2048)
            if data and data != b'exit\r\n':
                self.conn.send(data)
                print('{} sent: {}'.format(self.address, data))
            else:
                self.conn.close()
                return


def echo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 5555))
    sock.listen(10)
    while True:
        conn, address = sock.accept()
        Echo(conn, address).start()


if __name__ == "__main__":
    try:
        echo()
    except:
        KeyboardInterrupt: exit()
```

2. Using asyncio implement a HTTP/1.0 web file browser (nginx autoindex style).
  + The functions should includes: browsing directory, jumping, and open files. 
  + Editing directory and files are not asked to supported.
  + In this assignment, you need to use python3 asyncio stream to create a web file browser. 
  HTTP/1.0 should be used, because HTTP/1.1 supports keep-alive, 
  which makes our implementation more complex. When running in a directory, 
  the home page of your server should be the list of files and sub directories. 
  The functions should include: browsing directory, jumping, and open files. 
  Editing directory and files are not asked to supported An example is given like this.
  ![](./lab04_README_01.png)
  + Logic
    1. Your server should only support GET/HEAD method. For more details about the difference between GET and HEAD method, 
    please read the Lecture 03 slides. When receive other method (POST etc.), 
    you should return an error code `405 Method Not Allowed`.
    2. Remember to add `Connection: close` to your response header.
    3. When receive a request path, check if it is a directory. 
    You might want to add `./` to the client path to make sure you are working on current directory. 
    * path = `./` + header.get('path') If the path is a directory, render a html page with files and directories listed in it.
      + If the path is a file, return the file with a correct mime type. 
      If server cannot decide the mime type from the file extension (.exe, .mp3, setc.),
       the mime type should be `application/octet-stream`. 
      + If the path doesn't exist, return an error `404 Not Found`
      + `pathlib` might be helpful for doing path operation. `https://docs.python.org/3/library/pathlib.html`
  + Functions you might need
    1.  `os.listdir`
        This can list current directory or a given path.
    2.  `os.path.isfile` 
       This function can check if a path is a file.
    3. `os.path.getsize`
       This function can get the filesize in bytes, which might be useful if you want to add Content-Length to your response header.
    4. `open`
      Example:
      `file = open(name)`
      `writer.write(file.read())`
    Calling these function may raise FileNotFoundError Exception, you can organize your code like follow example:
``` python
try:
 # some server logic
except FileNotFoundError:
 # write 404 Not Found Response
```
  +  HTML Example
``` html
<html><head><title>Index of .//</title></head>
<body bgcolor="white">
<h1>Index of .//</h1><hr>
<pre>
<a href="dir1/">dir1/</a><br />
<a href="dir2/">dir2/</a><br />
<a href="file1">file1</a><br />
<a href="file1">file1</a><br />
</pre>
<hr>
</body></html>
```
![](./lab04_README_02.png)