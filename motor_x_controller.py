import RPi.GPIO as GPIO
import time

# GPIO 腳位設定
MOTOR_X_FORWARD = 17  # 馬達正轉控制腳位
MOTOR_X_BACKWARD = 18  # 馬達反轉控制腳位
LIMIT_SWITCH_LEFT = 22  # 左側限位開關
LIMIT_SWITCH_RIGHT = 23  # 右側限位開關

# GPIO 初始化
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_X_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_X_BACKWARD, GPIO.OUT)
GPIO.setup(LIMIT_SWITCH_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LIMIT_SWITCH_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def move_left():
    if GPIO.input(LIMIT_SWITCH_LEFT) == GPIO.HIGH:
        GPIO.output(MOTOR_X_FORWARD, GPIO.HIGH)
        GPIO.output(MOTOR_X_BACKWARD, GPIO.LOW)
    else:
        stop()

def move_right():
    if GPIO.input(LIMIT_SWITCH_RIGHT) == GPIO.HIGH:
        GPIO.output(MOTOR_X_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_X_BACKWARD, GPIO.HIGH)
    else:
        stop()

def stop():
    GPIO.output(MOTOR_X_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_X_BACKWARD, GPIO.LOW)