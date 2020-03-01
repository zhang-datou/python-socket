#  coding=utf-8
# -*- coding: utf-8 -*-
'''
@Descripttion: 
@version: 
@Author: Zhangjianqing
@Date: 2020-02-20 19:30:15
@LastEditors: Zhangjianqing
@LastEditTime: 2020-03-01 19:40:40
'''
import sys
import socket  # socket模块
import time
import threading
from threading import Thread, Lock

import json


class UdpServer(object):
    def __init__(self, address):
        # 连接global server
        self.address = address
        self.server = socket.socket(socket.AF_INET,
                                    socket.SOCK_DGRAM)  # 定义socket类型，网络通信，TCP
        self.server.bind(self.address)  # 套接字绑定的IP与端口
        print("Udp server start")

    def send_data(self, data):
        #
        self.server.sendto(data, self.address)

    def msg_thread(self):
        """
        接收新连接
        """
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=self.msg_handle)
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

    def msg_handle(self):
        global fp_config
        global config_params
        while True:
            # 接收来自客户端的数据
            recv_data, addr = self.server.recvfrom(1024)
            recv_data_json = json.loads(recv_data.decode())
            print(recv_data_json)
            try:
                msg_type = recv_data_json["msg_type"]
                tele_flag = recv_data_json["tele_flag"]
                if tele_flag:
                    # 接收
                    try:
                        config_params[msg_type] = recv_data_json[msg_type]
                        # 写
                        write_json_file(fp_config, config_params)
                    except Exception as e:
                        pass
                else:
                    # 发送
                    send_data = json.dumps(config_params[msg_type])
                    self.server.sendto(send_data, self.address)

            except Exception as e:
                pass
            finally:
                # 写
                write_json_file(fp_config, config_params)


def read_json_file(filepath):
    with open(filepath, 'r') as f:
        config_params = json.load(f)
    f.close()
    return config_params


def write_json_file(filepath, params):
    with open(filepath, 'w') as f:
        json.dump(params, f)
    f.close()


if __name__ == '__main__':
    print("client")
    cnt = 0

    fp_config = '/home/zhangjq/omh_robot/ros/remote_task/test/udp.json'
    # 读
    config_params = read_json_file(fp_config)

    # TODO:动态获取
    udp_server_addr = ('127.0.0.1', 9000)  # 本机IP
    udp_server = UdpServer(udp_server_addr)
    udp_server.msg_thread()

    while True:
        i = 5
