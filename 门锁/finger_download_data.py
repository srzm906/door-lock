#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

from upload_download_on_mysql import download_data

try:
    # 通过串口连接指纹模块
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)
    # 如指纹模块有密码则验证密码
    if ( f.verifyPassword() == False ):
       raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')

#打印已有指纹数和指纹总数
print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

try:
    ID = int(input('请输入新成员的指纹ID：'))
    # for循环目的是在新的指纹模块下载所有指纹数据
    # for ID in range(44):
    data = download_data(ID)
    #从数据库下载该指纹编号的特征值,eval()将str转换为list
    characteristic = eval(data[0])
    finger_id = int(data[1])
    print(finger_id, type(characteristic))
    # 将指纹特征值上载到指定的缓冲区，并返回布尔值决定是否上载成功
    t = f.uploadCharacteristics(FINGERPRINT_CHARBUFFER1, characteristic)
    if t:
        print("载入指纹数据成功！")
    else:
        print("载入指纹数据失败！")
        raise ValueError('The finger_data not download successfully!')
    # 将缓冲区的指纹特征储存为对应ID的指纹模板
    positionNumber = f.storeTemplate(finger_id)
    # 打印成功下载到指纹模块的指纹ID
    print('Now template position #' + str(positionNumber))
    time.sleep(0.5)
    print('指纹模板下载成功!')
except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)


