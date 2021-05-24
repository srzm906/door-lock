#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pymysql
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

import traceback

from upload_download_on_mysql import upload_data



def upload_single_finger_data():
    """
    @description : 上传单个指纹数据
    ---------
    @params :
    -------
    @Return :
    -------
    """
    try:
        # 通过串口连接指纹模块
        f = PyFingerprint('COM15', 57600, 0xFFFFFFFF, 0x00000000)
        # 如指纹模块有密码则验证密码
        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        exit(1)

    #打印已有指纹数和指纹总数
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    try:
        positionNumber = f.getTemplateCount()-1
        print('当前指纹ID为:',positionNumber)
        positionNumber = int(input("请输入指纹ID: "))

        # 将对应ID的指纹模板加载到缓冲区一
        f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)
        # 将缓冲区一的指纹模板生成指纹特征值
        characteristic = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
        # 打印特征值
        print(characteristic)
        # 根据指纹ID查找对应位置并更新指纹数据
        if(upload_data(characteristic, positionNumber)):
            time.sleep(0.5)
            print('上传指纹数据成功!')
        else:
            print("上传指纹数据失败!")
        
    except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            traceback.print_exc()
            # exit(1)





def upload_all_finger_data():
    """
    @description : 上传所有指纹数据，当调用此函数时需更改upload_download_on_mysql.py文件中注释的插入sql语句
    ---------
    @params :
    -------
    @Return :
    -------
    """
    try:

        # 通过串口连接指纹模块
        f = PyFingerprint('COM15', 57600, 0xFFFFFFFF, 0x00000000)
        # 如指纹模块有密码则验证密码
        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        exit(1)

    #打印已有指纹数和指纹总数
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    try:
        # 下面for循环是为了上传所有指纹数据到数据库,如
        for positionNumber in range(f.getTemplateCount()):

            # 将对应ID的指纹模板加载到缓冲区一
            f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)
            # 将缓冲区一的指纹模板生成指纹特征值
            characteristic = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
            # 打印特征值类型
            print(type(characteristic))
            # 记得修改代码！
            if(upload_data(characteristic, positionNumber)):
                time.sleep(0.5)
                print('上传指纹数据成功!')
            else:
                print("上传指纹数据失败!")
    
    except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            traceback.print_exc()
            #exit(1)
