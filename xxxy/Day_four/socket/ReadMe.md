# Python Socket 编程详解

Python 提供了两个基本的 socket 模块：

* `Socket` 它提供了标准的BSD Socket API。
* `SocketServer` 它提供了服务器重心，可以简化网络服务器的开发。

下面讲解下 Socket模块功能。
 
### Socket 类型
套接字格式：socket(family, type[,protocal]) 使用给定的套接族，套接字类型，协议编号（默认为0）来创建套接字

socket 类型 | 描述 
:--- | :---
socket.AF_UNIX | 用于同一台机器上的进程通信（既本机通信）
socket.AF_INET | 用于服务器与服务器之间的网络通信
socket.AF_INET6 | 基于IPV6方式的服务器与服务器之间的网络通信
socket.SOCK_STREAM | 基于TCP的流式socket通信
socket.SOCK_DGRAM | 基于UDP的数据报式socket通信
socket.SOCK_RAW | 原始套接字，普通的套接字无法处理ICMP、IGMP等网络报文，而SOCK_RAW可以；其次SOCK_RAW也可以处理特殊的IPV4报文；此外，利用原始套接字，可以通过IP_HDRINCL套接字选项由用户构造IP头
socket.SOCK_SEQPACKET | 可靠的连续数据包服务

创建TCP Socket：
``` Python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

创建UDP Socket：
``` Python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

### Socket 函数
* TCP发送数据时，已建立好TCP链接，所以不需要指定地址，而UDP是面向无连接的，每次发送都需要指定发送给谁。
* 服务器与客户端不能直接发送列表，元素，字典等带有数据类型的格式，发送的内容必须是字符串数据。

**服务器端 Socket 函数**

Socket 函数 | 描述
:--- | :---
s.bind(address) | 将套接字绑定到地址，在AF_INET下，以tuple(host, port)的方式传入，如s.bind((host, port))
s.listen(backlog) | 开始监听TCP传入连接，backlog指定在拒绝链接前，操作系统可以挂起的最大连接数，该值最少为1，大部分应用程序设为5就够用了
s.accpet() | 接受TCP链接并返回（conn, address），其中conn是新的套接字对象，可以用来接收和发送数据，address是链接客户端的地址。

**客户端 Socket 函数**

Socket 函数 | 描述
:--- | :---
s.connect(address) | 链接到address处的套接字，一般address的格式为tuple(host, port)，如果链接出错，则返回socket.error错误
s.connect_ex(address) | 功能与s.connect(address)相同，但成功返回0，失败返回errno的值

**公共 Socket 函数**

Socket 函数 | 描述
:--- | :---
s.recv(bufsize[, flag]) | 接受TCP套接字的数据，数据以字符串形式返回，buffsize指定要接受的最大数据量，flag提供有关消息的其他信息，通常可以忽略
s.send(string[, flag]) | 发送TCP数据，将字符串中的数据发送到链接的套接字，返回值是要发送的字节数量，该数量可能小于string的字节大小
s.sendall(string[, flag]) | 完整发送TCP数据，将字符串中的数据发送到链接的套接字，但在返回之前尝试发送所有数据。成功返回None，失败则抛出异常
s.recvfrom(bufsize[, flag]) | 接受UDP套接字的数据u，与recv()类似，但返回值是tuple(data, address)。其中data是包含接受数据的字符串，address是发送数据的套接字地址
s.sendto(string[, flag], address) | 发送UDP数据，将数据发送到套接字，address形式为tuple(ipaddr, port)，指定远程地址发送，返回值是发送的字节数
s.close() | 关闭套接字
s.getpeername() | 返回套接字的远程地址，返回值通常是一个tuple(ipaddr, port)
s.getsockname() | 返回套接字自己的地址，返回值通常是一个tuple(ipaddr, port)
s.setsockopt(level, optname, value) | 设置给定套接字选项的值
s.getsockopt(level, optname[, buflen]) | 返回套接字选项的值
s.settimeout(timeout) | 设置套接字操作的超时时间，timeout是一个浮点数，单位是秒，值为None则表示永远不会超时。一般超时期应在刚创建套接字时设置，因为他们可能用于连接的操作，如s.connect()
s.gettimeout() | 返回当前超时值，单位是秒，如果没有设置超时则返回None
s.fileno() | 返回套接字的文件描述
s.setblocking(flag) | 如果flag为0，则将套接字设置为非阻塞模式，否则将套接字设置为阻塞模式（默认值）。非阻塞模式下，如果调用recv()没有发现任何数据，或send()调用无法立即发送数据，那么将引起socket.error异常。
s.makefile() | 创建一个与该套接字相关的文件

### Socket 编程思想

**TCP 服务器**
1、创建套接字，绑定套接字到本地IP与端口
``` Python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind()
```

2、开始监听链接
``` Python
s.listen()
```

3、进入循环，不断接受客户端的链接请求
``` Python
While True:
    s.accept()
```

4、接收客户端传来的数据，并且发送给对方发送数据
``` Python
s.recv()
s.sendall()
```

5、传输完毕后，关闭套接字
``` Python
s.close()
```

**TCP 客户端**
1、创建套接字并链接至远端地址
``` Python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect()
```

2、链接后发送数据和接收数据
``` Python
s.sendall()
s.recv()
```

3、传输完毕后，关闭套接字

### Socket 编程实践之服务器端代码

``` Python
import socket

HOST = '192.168.1.100'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server start at: %s:%s' %(HOST, PORT)
print 'wait for connection...'

while True:
    conn, addr = s.accept()
    print 'Connected by ', addr

    while True:
        data = conn.recv(1024)
        print data

        conn.send("server received you message.")

# conn.close()
```

### Socket 编程实践之客户端代码

``` Python
import socket
HOST = '192.168.1.100'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = raw_input("Please input msg:")
    s.send(cmd)
    data = s.recv(1024)
    print data

    #s.close()
```