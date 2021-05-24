#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

def upload_data(data, id):
    try:
        # 连接数据库ip，端口号，用户名，密码
        con = pymysql.connect(host="10.18.52.156", port=3306, user='root', password="123456",
                              db='n6506', charset='utf8')
        # 生成cursor游标对象
        cursor = con.cursor()
        # 下面注释即为上传所有数据时的代码
        # try:
        #     # 插入指纹数据和指纹ID
        #     sql = 'insert into finger_data (data,finger_id) VALUES ("{}","{}");'.format(data, id)
        #     # 执行sql语句
        #     cursor.execute(sql)
        # except Exception as e:
        #     pass
        
        # sql语句：根据指纹ID更新指纹数据 
        sql = "update member1 set finger_data='{}' where finger_id='{}'".format(data,id)
        
        # 执行sql语句，返回
        a=cursor.execute(sql)
        print(a)
        con.commit()
        con.close()
        # 关闭连接
        return True
    except Exception as e:
        print("upload_data can not connect mysql")
        print(e)
        raise ("upload_data can not connect mysql")
        # return False



def download_data(ID):
    try:
        # 连接数据库ip，端口号，用户名，密码
        con = pymysql.connect(host="10.18.52.156", port=3306, user='root', password="123456",
                              db='n6506', charset='utf8')
        # 生成cursor游标对象
        cursor = con.cursor()
        # 根据指纹ID查询指纹数据
        sql = 'select  finger_data,finger_id from member where finger_id={};'.format(ID)
        # 执行sql语句
        num = cursor.execute(sql)
        # print(num)

        # 执行sql语句后得到元组（指纹数据，指纹ID）
        info = cursor.fetchone()
        # 提交到数据库
        con.commit()
        # 关闭连接
        con.close()
        return info
    except Exception as e:
        print(e)
        raise ("download_data can not connect mysql")
