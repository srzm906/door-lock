import socket
import sys
import time
import requests
import json
import traceback

# 
ERROR = 0

host = '10.18.52.156'
port = 6666

# socket 连接服务器
def client_to_server_by_socket(data):
    """
    data: 传送数据
    """
    try:
        # socket对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接服务器 (主机+端口)
        sock.connect((host, port))
    except socket.error as e:
        # 打印具体出错信息
        traceback.print_exc()
        # 报错返回 0
        return ERROR
    # 接受服务器发来信息

    r = sock.recv(1024)
    # decode() 以'utf-8'的编码格式解码字符串
    print(r.decode('utf-8'))

    # 向服务器发送数据
    # encode() 以'utf-8'的编码格式编码字符串
    sock.send(data.encode('utf-8'))

    # 接受服务器返回的判断结果或其他信息
    recv = sock.recv(1024).decode('utf-8')
    print(recv)
    # 关闭客户端
    sock.close()
    return recv