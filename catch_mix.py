import RPi.GPIO as GPIO
import pigpio
import time

# 腳位定義（使用實體腳位）
SERVO_PIN = 11     # GPIO17 → Pin 11（放線／收線馬達）
BUTTON_PIN = 13    # GPIO27 → Pin 13（按鈕）

# 爪子伺服腳位（pigpio 使用 BCM 編號）
CLAW_SERVO_PIN = 18  # GPIO18（爪子伺服控制用）

# 初始化 GPIO（放線／收線馬達）
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz 適合伺服馬達
pwm.start(0)

# 初始化 pigpio（爪子控制）
pi = pigpio.pi()
if not pi.connected:
    print("⚠️ 請先執行：sudo pigpiod")
    exit()

# 馬達控制函式（用 duty cycle 控制 PWM）
def set_servo_speed(duty_cycle):
    pwm.ChangeDutyCycle(duty_cycle)

# 爪子控制函式
def close_claw():
    print("🤖 爪子合起來")
    pi.set_servo_pulsewidth(CLAW_SERVO_PIN, 900)  # 收爪角度

def open_claw():
    print("🔓 爪子打開")
    pi.set_servo_pulsewidth(CLAW_SERVO_PIN, 1500)  # 張開角度

def stop_claw():
    pi.set_servo_pulsewidth(CLAW_SERVO_PIN, 0)  # 停止脈波輸出

try:
    print("等待按鈕觸發...")
    executed = False

    while not executed:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            print("✅ 按鈕按下，立即放線...")

            # 放線
            set_servo_speed(4.2)
            time.sleep(6)
            set_servo_speed(7.5)
            print("🧵 放線完成")

            # 等 1 秒再收爪
            time.sleep(1)
            close_claw()
            print("⏳ 爪子已收合，等待 3 秒...")
            time.sleep(3)

            # 收線
            print("🔄 開始收線...")
            set_servo_speed(9.0)
            time.sleep(6.5)
            set_servo_speed(7.5)
            print("✅ 收線完成")

            # 等 6 秒再打開爪子
            time.sleep(6)
            open_claw()
            print("🔓 爪子已打開，流程結束")

            executed = True

        time.sleep(0.01)

except KeyboardInterrupt:
    print("🛑 手動中斷程式")

finally:
    pwm.stop()
    GPIO.cleanup()
    pi.stop()
