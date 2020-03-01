#  coding=utf-8
# -*- coding: utf-8 -*-
'''
@Descripttion: 
@version: 
@Author: Zhangjianqing
@Date: 2020-02-20 19:30:15
@LastEditors: Zhangjianqing
@LastEditTime: 2020-03-01 19:39:43
'''
import sys
import socket  # socket模块
import time
import threading
from threading import Thread, Lock

import json
import struct


class TcpClient(object):
    def __init__(self, address):  # 连接
        self.address = address
        self.client = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        self.client.connect(self.address)  # 要连接的IP与端口

        print("Tcp client start")

    def send(self):
        global send_data  # 全局变量

        while True:
            try:
                self.client.sendall(send_data)

            except Exception as e:
                pass

            time.sleep(0.1)

    def recv(self):
        global recv_data  # 全局变量
        while True:
            try:
                # 1、接收报文头的长度
                header_size = struct.unpack('i', self.client.recv(4))[0]
                # 2、接收报文
                header_bytes = self.client.recv(header_size)

                # 3、解析报文
                header_json = header_bytes.decode('utf-8')
                header_dic = json.loads(header_json)
                print(header_dic)

                # 4、获取真实数据的长度
                data_size = header_dic['data_size']

                # 5、获取数据
                recv_size = 0
                res = b''
                while recv_size < data_size:
                    recv_date = self.client.recv(1024)
                    res += recv_date
                    recv_size += len(recv_date)
                print(res)
                # recv_data = self.client.recv(1024)
            except Exception as e:
                pass

            time.sleep(0.1)

    def start(self):  # 连接
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=self.send)
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=self.recv)
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

    def msg_handle(self):

        cnt = 0
        while True:
            # 发送
            cnt = (cnt + 1) % 10000
            try:
                self.client.sendall(str(cnt))

            except Exception as e:
                pass

            # 接收
            try:
                recv_data = self.client.recv(1024)

                recv_data_json = json.loads(recv_data.decode())
                print(recv_data)
                print('recv:', recv_data_json['url'])
                time.sleep(0.1)

            except Exception as e:
                pass


if __name__ == '__main__':

    cnt = 0

    send_data = str(cnt)
    recv_data = 0  # 全局变量

    server_addr = ('127.0.0.1', 8000)
    tcp_client = TcpClient(server_addr)
    tcp_client.start()

    while True:
        print("send", send_data)
        print("recv", recv_data)
        cnt = cnt + 1
        send_data = str(cnt)
        time.sleep(1)
