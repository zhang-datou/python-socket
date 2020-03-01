# coding=utf-8
# -*- coding: utf-8 -*-
'''
@Descripttion: 
@version: 
@Author: Zhangjianqing
@Date: 2020-02-20 14:31:07
@LastEditors: Zhangjianqing
@LastEditTime: 2020-03-01 19:39:27
'''
import socket  # socket模块
import json
import time
import threading
from threading import Thread, Lock

import struct
'''
一对多
'''


class TcpServer(object):
    def __init__(self, address):  # 连接
        self.server = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        self.server.bind(address)  # 套接字绑定的IP与端口
        self.server.listen(5)  # 开始TCP监听

        # self.client_listen()  #监听一个客户端

        thread = Thread(target=self.listen_thread)  # 一直监听
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

        print("Tcp server start")

    def client_listen(self):
        """
        接收新连接
        """
        global conn_pool

        self.client, _ = self.server.accept()  # 阻塞，等待客户端连接
        # 加入连接池
        conn_pool.append(self.client)

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

    def listen_thread(self):
        """
        监听线程
        """

        while True:
            self.client_listen()

    def send(self):
        global send_data  # 全局变量
        global conn_pool

        # TODO:加锁
        while True:
            try:

                # 1、制作报头
                header_dic = {
                    'data_size': len(send_data),
                    'md5': 'dgdsfsdfdsdfsfewrewge'
                }
                header_json = json.dumps(header_dic)
                header_bytes = header_json.encode('utf-8')
                # 2、先发送报头的长度
                header_size = len(header_bytes)
                self.client.send(struct.pack('i', header_size))
                # 3、发送报头
                self.client.send(header_bytes)
                # 4、发送真实的数据
                self.client.send(send_data)
            except Exception as e:
                # 连接断开,删除连接
                conn_pool.remove(self.client)
                self.client.close()
                print("A client disconnect")
                break

            time.sleep(0.1)

    def recv(self):
        global recv_data  # 全局变量
        global conn_pool
        # TODO:加锁
        while True:
            try:
                recv_data = self.client.recv(1024)
            except Exception as e:
                # 连接断开
                break

            time.sleep(0.1)


if __name__ == '__main__':

    cnt = 0
    send_data = str(cnt)
    recv_data = 0  # 全局变量

    conn_pool = []  # 连接池
    server_addr = ('127.0.0.1', 8000)  # 本机IP
    tcp_server = TcpServer(server_addr)

    while True:
        cnt = cnt + 1

        print("num", len(conn_pool))
        # TCP测试
        print("send", send_data)
        print("recv", recv_data)
        send_data = str(cnt)

        time.sleep(1)
