#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from test_to_server import send_data
from pi_control import *
import mfrc522
GPIO.setwarnings(False)
print(mfrc522)
try:
    reader = SimpleMFRC522()
except Exception as e:
    print(e)

try:
    try:
        while True:
                print('Waiting for your card...')
                card_id= reader.read_id()
                if card_id:
                    res = send_data(card_id=card_id)
                    print(res,type(res))
                if(res=='aaaaa'):
                    print("sss")
                    sound_1()
                elif res =='bbbbb':
                    sound_3()
                else:
                    sound_2()

                print(card_id)
                time.sleep(0.5)
    except Exception as e:
        print(e)
        pass
except KeyboardInterrupt as e:
        GPIO.cleanup()
        exit(1)
