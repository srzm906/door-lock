#!/usr/bin/env python
# -*- coding: utf-8 -*-
#指纹注册
import time


from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

from data_to_server import client_to_server_by_socket as client_to_server 
from upload_download_on_mysql import upload_data



name = input('请输入您的姓名：')
# phone = input('请输入您的手机号: ')
try:
    # 通过串口连接指纹模块
    f = PyFingerprint('COM15', 57600, 0xFFFFFFFF, 0x00000000)
    # 如指纹模块有密码则验证密码
    if ( f.verifyPassword() == False ):
       raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    exit(1)

# 打印当前指纹模块共有多少指纹  
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to enroll new finger
try:
    print('Waiting for finger...')

    #等待指纹的读取
    while ( f.readImage() == False ):
        pass

    #将读取的指纹特征值存入缓存区一
    f.convertImage(FINGERPRINT_CHARBUFFER1)

    #检查指纹是否读取成功
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Keep for your finger...')
    time.sleep(1)
    #再次读取相同指纹
    print('Waiting for same finger again...')

    #等待指纹的读取
    while ( f.readImage() == False ):
        pass

    #将读取的指纹特征值存入缓存区二
    f.convertImage(FINGERPRINT_CHARBUFFER2)

    #比较两缓存区的指纹特征值是否相同
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    #创建新的指纹模板
    f.createTemplate()

    #保存指纹模板，并返回指纹ID
    positionNumber = f.storeTemplate()

    time.sleep(0.2)
    # 下载指纹特征值
    characteristic = f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
    # 打印指纹特征值
    print(characteristic,type(characteristic))
    # 上传指纹ID，格式为如下：
    data = ('01'+name+','+str(positionNumber))
    recv = client_to_server(data)

    # 上传指纹数据
    upload_data(characteristic,positionNumber)
    time.sleep(0.5)
    
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
