#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 树莓派GPIO包
# import RPi.GPIO as GPIO
import time
import traceback

# 此延时目的是在树莓派 sudo crontab -e 开机自启动是起延时作用
time.sleep(5)

# 导入指纹库
from pyfingerprint.pyfingerprint import PyFingerprint
# FINGERPRINT_CHARBUFFER1为指纹模块缓冲区 1区
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1

# 签到情况根据蜂鸣器声响决定
# from pi_control import sound_1,sound_2,sound_3,open_door
# 下位机发送数据给服务器
from data_to_server import client_to_server_by_socket as client_to_server 

# GPIO引脚占用报错屏蔽
# GPIO.setwarnings(False)

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

try:
    while True:
        # 搜索指纹
        try:
            print('Waiting for finger...')

            # 等待指纹读取
            while ( f.readImage() == False ):
                pass

            # 将读取指纹的特征值存入缓存区一
            f.convertImage(FINGERPRINT_CHARBUFFER1)

            # 搜索指纹模板
            result = f.searchTemplate()

            # 指纹位置
            positionNumber = result[0]
            # 指纹分数
            accuracyScore = result[1]

            # 指纹ID为-1证明未匹配到指纹
            if ( positionNumber == -1 ):
                print('No match found!')
                # exit(0)
                pass
            else:
                # 发送到服务器的数据
                data = ('000'+str(positionNumber))
                # 服务器返回的数据
                res = client_to_server(data)
                # 如果为open_door,则为开门
                if(res=='open_door'):
                    print('开门')
                    # open_door()
                """
                # 此段注释为考勤代码
                # 发送到服务器的数据
                data = ('00b'+str(positionNumber))
                # 服务器返回的数据
                res = client_to_server(data)
                if(res=='aaaaa'):
                    print("1")
                    # sound_1()
                    #签到成功蜂鸣器短鸣0.5s
                elif res =='bbbbb':
                    print("2")
                    # sound_3()
                    #签退成功蜂鸣器长鸣1s
                else:
                    print("3")
                    # sound_2()
                    #无法识别蜂鸣器短鸣两声
                """
                print('Found template at position #' + str(positionNumber))
                # print('The accuracy score is: ' + str(accuracyScore))
        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))
            continue

except KeyboardInterrupt as e:
    exit(1)
