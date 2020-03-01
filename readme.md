<!--
 * @Descripttion: 
 * @version: 
 * @Author: Zhangjianqing
 * @Date: 2020-03-01 19:15:05
 * @LastEditors: Zhangjianqing
 * @LastEditTime: 2020-03-01 19:58:18
 -->
基于Python实现简单的tcp和udp传输功能，可以发送自定义数据格式，支持一对多模式。

## tcp

### server
设定IP和端口建立socket实例化对象
```Python
server_addr = ('192.168.131.146', 8000)  #本机IP
tcp_server = TcpServer(server_addr)
```
创建监听线程，用于监听客户端的连接。并将客户端加入连接池中
```Python
thread = Thread(target=self.listen_thread)

self.client, _ = self.server.accept()  # 阻塞，等待客户端连接
# 加入连接池
conn_pool.append(self.client)
 ```
在监听线程中，监听到客户端后，创建与该客户端的发送与接收线程。
```Python
thread = Thread(target=self.send)
thread = Thread(target=self.recv)
 ```
 当客户端退出时，删除之
 ```Python
conn_pool.remove(self.client)
self.client.close()
 ```

### client
设定服务端IP和端口后，建立发送与接收线程 
```Python
tcp_client = TcpClient(server_addr)
tcp_client.start()


thread = Thread(target=self.send)
thread = Thread(target=self.recv)
 ```

## udp
udp部分增加json数据的传输，从文件中读取，后者客户端可进行更改。
### server
设定IP和端口建立实例化对象并创建接收信息的线程
```Python
udp_server = UdpServer(udp_server_addr)
udp_server.msg_thread()
```
接收json数据
```Python
recv_data, addr = self.server.recvfrom(1024)
recv_data_json = json.loads(recv_data.decode())
```
### client
设定IP和端口建立实例化对象
```Python
socket_robot = UdpClient(robot_addr)
```
读取json数据并发送
```Python
config_params = json.dumps(config_params)#触发方式可使用按键事件
socket_robot.send_data(config_params)
```

注：python2版本，有bug或者描述有问题的地方请见谅。