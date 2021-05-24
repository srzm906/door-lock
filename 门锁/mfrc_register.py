#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal
import sys
import RPi.GPIO as GPIO

import traceback
from mfrc522 import SimpleMFRC522
from data_to_server import client_to_server_by_socket as client_to_server 
from pi_control import sound_1
from test_to_server import create_member_info


GPIO.setwarnings(False)
name = input('请输入您的姓名：')
try:
    reader = SimpleMFRC522()
except Exception as e:
    print(e)

try: 
    print('Waiting for your card...')
    card_id= reader.read_id()
    if card_id:
        data = create_member_info(name=name,card_id=card_id)
        #按照姓名向数据库发送卡号
        res =data['card_id']
        if res!=0:
            sound_1()
        #print(data)
except Exception as e:
        #print(e)
        traceback.print_exc()
        exit(1)
