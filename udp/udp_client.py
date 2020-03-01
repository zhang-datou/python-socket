# coding=utf-8
# -*- coding: utf-8 -*-
'''
@Descripttion: 
@version: 
@Author: Zhangjianqing
@Date: 2020-02-20 14:31:07
@LastEditors: Zhangjianqing
@LastEditTime: 2020-03-01 19:40:32
'''
import socket  # socket模块
import json
import time
import threading
from threading import Thread, Lock
'''
一对多
'''


class UdpClient(object):
    def __init__(self, address):  # 连接
        self.address = address
        self.client = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)  # 定义socket类型，网络通信，TCP
        print("Udp client start")

    def send_data(self, data):
        self.client.sendto(data, self.address)

    def recv_data(self):
        recv_data = self.client.recv(1024)
        return recv_data


if __name__ == '__main__':

    server_addr = ('127.0.0.1', 8000)  # 本机IP
    robot_addr = ('127.0.0.1', 9000)  # 小车IP和端口

    socket_robot = UdpClient(robot_addr)

    config_params = {
        "tele_flag": True,
        "msg_type": "host",
        "host": {
            "ip": server_addr[0],
            "port": server_addr[1]
        }
    }
    config_params = json.dumps(config_params)
    # 触发方式可使用按键事件
    socket_robot.send_data(config_params)

    cnt = 0
    while True:
        cnt = cnt + 1
        # UDP测试
        socket_robot.send_data(str(cnt))
        socket_robot.send_data(config_params)

        time.sleep(1)
