import RPi.GPIO as GPIO
import time

# GPIO 腳位設定
MOTOR_Y_FORWARD = 24  # 馬達正轉控制腳位
MOTOR_Y_BACKWARD = 25  # 馬達反轉控制腳位
LIMIT_SWITCH_FRONT = 5  # 前側限位開關
LIMIT_SWITCH_BACK = 6  # 後側限位開關

# GPIO 初始化
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_Y_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_Y_BACKWARD, GPIO.OUT)
GPIO.setup(LIMIT_SWITCH_FRONT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LIMIT_SWITCH_BACK, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def move_forward():
    if GPIO.input(LIMIT_SWITCH_FRONT) == GPIO.HIGH:
        GPIO.output(MOTOR_Y_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_Y_BACKWARD, GPIO.LOW)
    else:
        stop()

def move_backward():
    if GPIO.input(LIMIT_SWITCH_BACK) == GPIO.HIGH:
        GPIO.output(MOTOR_Y_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_Y_BACKWARD, GPIO.HIGH)
    else:
        stop()

def stop():
    GPIO.output(MOTOR_Y_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_Y_BACKWARD, GPIO.LOW)