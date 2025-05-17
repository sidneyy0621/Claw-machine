# 控制爪子打開、關閉、上升、下降，以及抓取
# 當抓取按鈕被按下時，執行一個完整的抓取流程：
# 爪子下降。
# 爪子關閉（抓取物品）。
# 爪子上升。
# 爪子打開（釋放物品）。

import RPi.GPIO as GPIO
import time
import motor_x_controller
import motor_y_controller

# GPIO 腳位設定
CLAW_OPEN_PIN = 20       # 控制爪子打開的腳位
CLAW_CLOSE_PIN = 21      # 控制爪子關閉的腳位
CLAW_UP_PIN = 19         # 控制爪子上升的腳位
CLAW_DOWN_PIN = 26       # 控制爪子下降的腳位
GRAB_BUTTON_PIN = 13     # 抓取按鈕的腳位

# GPIO 初始化
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLAW_OPEN_PIN, GPIO.OUT)
GPIO.setup(CLAW_CLOSE_PIN, GPIO.OUT)
GPIO.setup(CLAW_UP_PIN, GPIO.OUT)
GPIO.setup(CLAW_DOWN_PIN, GPIO.OUT)
GPIO.setup(GRAB_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def open_claw():
    GPIO.output(CLAW_OPEN_PIN, GPIO.HIGH)
    GPIO.output(CLAW_CLOSE_PIN, GPIO.LOW)
    time.sleep(0.5)
    stop_claw()

def close_claw():
    GPIO.output(CLAW_OPEN_PIN, GPIO.LOW)
    GPIO.output(CLAW_CLOSE_PIN, GPIO.HIGH)
    time.sleep(0.5)
    stop_claw()

def move_up():
    GPIO.output(CLAW_UP_PIN, GPIO.HIGH)
    GPIO.output(CLAW_DOWN_PIN, GPIO.LOW)
    time.sleep(1)
    stop_claw()

def move_down():
    GPIO.output(CLAW_UP_PIN, GPIO.LOW)
    GPIO.output(CLAW_DOWN_PIN, GPIO.HIGH)
    time.sleep(1)
    stop_claw()

def stop_claw():
    GPIO.output(CLAW_OPEN_PIN, GPIO.LOW)
    GPIO.output(CLAW_CLOSE_PIN, GPIO.LOW)
    GPIO.output(CLAW_UP_PIN, GPIO.LOW)
    GPIO.output(CLAW_DOWN_PIN, GPIO.LOW)

def move_to_hole():
    print("移動到洞口...")
    motor_x_controller.move_right()
    motor_y_controller.move_forward()
    time.sleep(2)  # 模擬移動時間
    motor_x_controller.stop()
    motor_y_controller.stop()

def return_to_start():
    print("返回初始位置...")
    motor_x_controller.move_left()
    motor_y_controller.move_backward()
    time.sleep(2)  # 模擬移動時間
    motor_x_controller.stop()
    motor_y_controller.stop()

def grab_sequence(channel):
    print("抓取按鈕被按下，開始抓取流程。")
    move_down()    # 爪子向下移動
    close_claw()   # 爪子閉合（抓取物品）
    move_up()      # 爪子向上移動
    move_to_hole() # 移動到洞口
    open_claw()    # 爪子打開（釋放物品）
    return_to_start() # 返回初始位置
    print("抓取流程完成。")

# 設定按鈕事件偵測
GPIO.add_event_detect(GRAB_BUTTON_PIN, GPIO.FALLING, callback=grab_sequence, bouncetime=300)