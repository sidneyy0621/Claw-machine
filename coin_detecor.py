# coin_detector.py

import RPi.GPIO as GPIO
import time

# 設定 GPIO 腳位號碼（BCM 模式）
COIN_PIN = 17  # 根據您的實際接線調整

def setup_coin_detector(callback):
    """
    設定投幣偵測器，當偵測到投幣時，呼叫指定的回呼函式。
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(COIN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # 當偵測到下降沿（投幣事件）時，呼叫 callback 函式
    GPIO.add_event_detect(COIN_PIN, GPIO.FALLING, callback=callback, bouncetime=300)

def cleanup():
    """
    清除 GPIO 設定。
    """
    GPIO.cleanup()
