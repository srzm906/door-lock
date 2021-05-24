#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time


def open_door():

    door_pin = 12
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(door_pin, GPIO.OUT)
    GPIO.output(door_pin, GPIO.HIGH)
    if GPIO.input(door_pin):
        print('Input was HIGH')
    else:
        print('Input was LOW')
    time.sleep(1)
    GPIO.output(door_pin, GPIO.LOW)
    if GPIO.input(door_pin):
        print('Input was HIGH')
    else:
        print('Input was LOW')
    GPIO.cleanup()


def sound_1():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    buzzer = 11
    GPIO.setup(buzzer, GPIO.OUT)
    buzz = GPIO.PWM(buzzer, 500)
    buzz.start(50)
    buzz.ChangeFrequency(1000)
    time.sleep(0.1)
    buzz.stop()
    #GPIO.output(buzzer, 0)
    GPIO.cleanup()

def sound_2():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    buzzer = 11
    GPIO.setup(buzzer, GPIO.OUT)
    buzz = GPIO.PWM(buzzer, 500)
    buzz.start(50)
    buzz.ChangeFrequency(1000)
    time.sleep(0.1)
    buzz.stop()
    time.sleep(0.15)
    buzz.start(50)
    buzz.ChangeFrequency(1000)
    time.sleep(0.1)
    buzz.stop()
    #GPIO.output(buzzer, 0)
    GPIO.cleanup()

def sound_3():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    buzzer = 11
    GPIO.setup(buzzer, GPIO.OUT)
    buzz = GPIO.PWM(buzzer, 500)
    buzz.start(50)
    buzz.ChangeFrequency(1000)
    time.sleep(0.4)
    buzz.stop()
    GPIO.output(buzzer, 0)
    GPIO.cleanup()