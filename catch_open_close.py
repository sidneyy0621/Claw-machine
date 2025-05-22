import RPi.GPIO as GPIO
import time

# 腳位定義（使用實體腳位）
SERVO_PIN = 11     # GPIO17 → Pin 11（橙線）
BUTTON_PIN = 13    # GPIO27 → Pin 13（按鈕）

# 初始化 GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 上拉電阻

# 設定 PWM（50Hz 適合伺服馬達）
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# 馬達控制函式
def set_servo_speed(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)

try:
    print("等待按鈕觸發...")
    executed = False

    while not executed:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # 按下按鈕（LOW）
            print("✅ 按鈕按下，立即放線...")

            # 放線方向（例如 4.5，視你馬達調整）
            set_servo_speed(4.2)
            time.sleep(6)  # 約轉 15 圈（視你的馬達微調時間）
            set_servo_speed(7.5)  # 停止
            print("🧵 放線完成，等待 3 秒...")

            time.sleep(3)

            # 收線方向（例如 9.0，與放線反方向）
            print("🔄 開始收線...")
            set_servo_speed(9.0)
            time.sleep(6)  # 收回來
            set_servo_speed(7.5)  # 停止
            print("✅ 收線完成，流程結束。")

            executed = True

        time.sleep(0.01)  # 快速檢查按鈕狀態

except KeyboardInterrupt:
    print("中斷程式")

finally:
    pwm.stop()
    GPIO.cleanup()
