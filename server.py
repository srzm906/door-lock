#! /usr/bin/env python3
# _*_ coding:utf-8 _*_

import socket
import sys
import threading
import pymysql
import time
import traceback
#import requests


class Server:
    def __init__(self, host_addr='127.0.0.1', port=6667,mysql_db='test'):
        self.host_addr = host_addr
        self.port = port
        self.sock = None
        self.addr = None
        self.mysql_port = 3306
        self.mysql_db = mysql_db

    def init(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.host_addr, self.port))
            self.sock.listen()
        except socket.error as e:
            print(e)
            sys.exit()
        print("服务器初始化成功，等待连接...")

    def accept_client(self):
        # 等待客户端连接
        while True:
            conn, addr = self.sock.accept()
            self.addr = addr
            print("客户端IP：{}已连接,端口为:{}！".format(self.addr[0],self.addr[1]))
            # 创建一个子线程对象
            t = threading.Thread(target=self.handle_message, args=(conn,))
            t.setDaemon(True)
            t.start()

    def handle_message(self, client):
        """
        @description :处理客户端的数据
        ---------
        @params :client客户端对象，由创建子线程对象时传入
        -------
        @Return :
        -------
        """
        client.sendall('连接服务器成功！'.encode('utf-8'))
        try:
          while True:
            data = client.recv(1024).decode('utf-8')
            data = data.replace('(', '').replace(')', '')
            #print(data)
            # data[0]用于判断指纹还是校园卡 data[1]用于判断门禁还是注册
            if not data:
                break
            if data[0] == '0':
                if data[1]=='0':
                    print('指纹开锁通道')
                    replay=self.finger_db(data[2:])
                    self.send_message(replay,client)
                elif data[1]=='1':
                    print('指纹录入系统中！')
                    self.finger_enroll(data[2:])
                    client.send('完成'.encode('utf-8'))
            elif data[0] == '1':
                if data[1]=='0':
                   print('rfid开锁通道')
                   replay=self.card_db(data[2:])
                   # print(replay,type(replay))
                   self.send_message(replay,client)
                elif data[1] == '1':
                    print('卡号录入系统')
                    self.card_enroll(data[2:])
                    client.send('已录入！'.encode('utf-8'))        
            else:
                print('unknown data!')
                break
          client.close()
          print('IP:{}已下线！'.format(self.addr))
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def send_message(replay, client):
        replay = str(replay)    
        client.send(replay.encode('utf-8'))

    def finger_db(self, finger_id):
        """
        @description :进入实验室的数据存入数据库
        ---------
        @params :指纹id
        -------
        @Return :
        -------
        """
        flag = finger_id[0]
        print(finger_id)
        finger_id=finger_id[1:]
        try:
            date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql ='insert into entry_records (time,finger_id) VALUES ("{}","{}");'.format(str(date_time), finger_id)
            self.connect_mysql(sql=sql)
            sql = "select name,finger_id from member1 where finger_id='{}'".format(finger_id)
            name_id = self.connect_mysql(sql=sql)
            if flag=='b':
                 recv_check=self.check_the_absence(name_id[0])
            else :
                recv_check="not door"
            # print(name_id)
            if name_id:
                 sql="update entry_records set name='{}' where time='{}'".format(name_id[0],date_time)
                 self.connect_mysql(sql=sql)     
            return recv_check
        # 关闭连接
        except Exception as e:
            traceback.print_exc()
            print("finger_db can not connect mysql")
            return 0

    def card_db(self, card_id):
        """
        @description :进入实验室的数据存入数据库
        ---------
        @params :卡号
        -------
        @Return :
        -------
        """
        # print(card_id)
        flag=card_id[0]
        card_id=card_id[1:]
        try:
            # 将卡号和进入时间存入数据库
            date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql = 'insert into entry_records (time,card_id) VALUES ("{}","{}");'.format(str(date_time), card_id)
            self.connect_mysql(sql=sql)
            # 将姓名卡号从数据库读取出来
            sql = "select name,card_id from member1 where card_id={}".format(card_id)   
            name_card = self.connect_mysql(sql=sql) 
            if flag=='b':
                 recv_check = self.check_the_absence(name_card[0])
            elif name_card:
               recv_check="not door"
            else:
               recv_check='0'
            print(name_card)
            if name_card:
                 sql="update entry_records set name='{}' where time='{}'".format(name_card[0],date_time)
                 self.connect_mysql(sql=sql)
            # 关闭连接
            return recv_check
        except Exception as e:
            traceback.print_exc()
            print("card_db can not connect mysql")
            return 0

    def finger_enroll(self, data):
        """
        @description :指纹注册
        ---------
        @params :名字和指纹编号
        -------
        @Return :无
        -------
        """
        data=data.split(',')
        print(data)
        try:
            sql = """update member1 set finger_id='{}' where name='{}'""".format(data[1], data[0])
            self.connect_mysql(sql=sql)
        except Exception as e:
            traceback.print_exc()

    def card_enroll(self,data):
        """
        @description :注册校园卡
        ---------
        @params :卡号和姓名
        -------
        @Return :无
        -------
        """
        data=data.split(',')
        print(data)
        try:
            sql = """update member1 set card_id='{}' where name='{}'""".format(data[1], data[0])
            self.connect_mysql(sql=sql)
        except Exception as e:
            traceback.print_exc()

    def check_the_absence(self,name):
        import requests
        """
        @description :签到签退
        ---------
        @params :名字
        -------
        @Return :后端的状态值 a表示签到，b表示签退，nnn表示无法识别
        -------
        """
        sql="select cardId from user where userName='{}'".format(name)
        card_id=self.connect_mysql(sql=sql,host='10.18.52.137',password='rootmysql',db='labmanage')
        print(card_id)
        if card_id:
            cardId={"cardId":card_id[0]}
            r=requests.post('http://10.18.52.137:8888/laboratory/sign',data=cardId)
            print(r.text)
            return r.text
        else:
            return 'nnn'

    def connect_mysql(self,sql,host='127.0.0.1',password='rootmysql',db='n6506'):
        # 连接数据库ip，端口号，用户名，密码
        con = pymysql.connect(host=host, port=3306, user='root', password=password,
                              db=db, charset='utf8')
        cursor = con.cursor()
        cursor.execute(sql)
        r=cursor.fetchone()
        #print(r,type(r))
        con.commit()
        con.close()
        return r

    def main(self):
        self.init()
        self.accept_client()

if __name__ == '__main__':
    try:
        Server('10.18.52.137',mysql_db='n6506',port=6666).main()
    except KeyboardInterrupt as e:
        print("服务器退出！")
        exit(0)
