#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pymysql


host = '10.18.52.156'

#在数据库中直接创建一个新成员
def create_member(name, stu_num,db='test'):
    """
    @description : 用于创建数据库内新成员
    ---------
    @params : name、phone为新成员姓名、手机号，db为所用数据库
    -------
    @Return : 
    -------
    """
    try:
        # 连接数据库
        con = pymysql.connect(host= host, port=3306, user='root', password="123456",
                                db=db, charset='utf8')
        # 创建游标对象
        cursor = con.cursor()
        # 此sql语句目的为插入一条新的数据
        sql = """insert into member1 (name,stu_num) values (%s,%s)"""
        # 执行sql语句
        cursor.execute(sql, (name,stu_num))
        # 提交到数据库
        con.commit() 
        # 关闭与数据库的连接
        con.close()
    except Exception as e:
        print(e)
        exit(1)
if __name__ == '__main__':
     name=input('请输入名字：')
     stu_num = input('请输入学号：')
     create_member(name, stu_num, db='n6506')
     print('录入成功！')
