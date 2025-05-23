import RPi.GPIO as GPIO
import time

# === 腳位定義 ===
COIN_SENSOR = 21       # 投幣感測器
BUZZER = 26            # 音樂蜂鳴器
X_IN1, X_IN2, X_EN = 17, 27, 18
Y_IN1, Y_IN2, Y_EN = 22, 23, 24
Z_SERVO = 20           # 放線伺服
CLAW_SERVO = 12        # 收爪伺服
BTN_UP = 5
BTN_DOWN = 6
BTN_LEFT = 13
BTN_RIGHT = 19
BTN_ACTION = 16        # 放線/放爪按鈕
CLAW_CLOSED = 3.0
CLAW_OPEN = 7.0

# === GPIO 初始化 ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in [X_IN1, X_IN2, X_EN, Y_IN1, Y_IN2, Y_EN, CLAW_SERVO, Z_SERVO, BUZZER]:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_ACTION, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COIN_SENSOR, GPIO.IN)

x_pwm = GPIO.PWM(X_EN, 1000)
y_pwm = GPIO.PWM(Y_EN, 1000)
claw_pwm = GPIO.PWM(CLAW_SERVO, 50)
z_pwm = GPIO.PWM(Z_SERVO, 50)
buzz_pwm = GPIO.PWM(BUZZER, 440)

x_pwm.start(0)
y_pwm.start(0)
claw_pwm.start(0)
z_pwm.start(0)
buzz_pwm.start(0)

# === 功能函式 ===

def play_music():
    buzz_pwm.ChangeDutyCycle(50)
    buzz_pwm.ChangeFrequency(440)
    time.sleep(1)
    buzz_pwm.ChangeDutyCycle(0)

def close_claw():
    claw_pwm.ChangeDutyCycle(CLAW_CLOSED)
    time.sleep(0.5)
    claw_pwm.ChangeDutyCycle(0)

def open_claw():
    claw_pwm.ChangeDutyCycle(CLAW_OPEN)
    time.sleep(0.5)
    claw_pwm.ChangeDutyCycle(0)

def lower_hook():
    z_pwm.ChangeDutyCycle(4.5)
    time.sleep(1)
    z_pwm.ChangeDutyCycle(7.5)

def raise_hook():
    z_pwm.ChangeDutyCycle(9.0)
    time.sleep(1)
    z_pwm.ChangeDutyCycle(7.5)

def stop_motors():
    GPIO.output(X_IN1, GPIO.LOW)
    GPIO.output(X_IN2, GPIO.LOW)
    GPIO.output(Y_IN1, GPIO.LOW)
    GPIO.output(Y_IN2, GPIO.LOW)
    x_pwm.ChangeDutyCycle(0)
    y_pwm.ChangeDutyCycle(0)

# === 主程式邏輯 ===

try:
    while True:
        print("💰 等待投幣...")
        while GPIO.input(COIN_SENSOR) == GPIO.HIGH:
            time.sleep(0.1)

        print("✅ 投幣成功！播放音樂")
        play_music()

        print("🎮 遊戲開始（35 秒）")
        close_claw()
        start_time = time.time()
        claw_opened = False
        action_triggered = False

        while time.time() - start_time < 35:
            # 移動控制
            if GPIO.input(BTN_LEFT) == GPIO.LOW:
                GPIO.output(X_IN1, GPIO.LOW)
                GPIO.output(X_IN2, GPIO.HIGH)
                x_pwm.ChangeDutyCycle(100)
            elif GPIO.input(BTN_RIGHT) == GPIO.LOW:
                GPIO.output(X_IN1, GPIO.HIGH)
                GPIO.output(X_IN2, GPIO.LOW)
                x_pwm.ChangeDutyCycle(100)
            else:
                GPIO.output(X_IN1, GPIO.LOW)
                GPIO.output(X_IN2, GPIO.LOW)
                x_pwm.ChangeDutyCycle(0)

            if GPIO.input(BTN_UP) == GPIO.HIGH:
                GPIO.output(Y_IN1, GPIO.HIGH)
                GPIO.output(Y_IN2, GPIO.LOW)
                y_pwm.ChangeDutyCycle(100)
            elif GPIO.input(BTN_DOWN) == GPIO.HIGH:
                GPIO.output(Y_IN1, GPIO.LOW)
                GPIO.output(Y_IN2, GPIO.HIGH)
                y_pwm.ChangeDutyCycle(100)
            else:
                GPIO.output(Y_IN1, GPIO.LOW)
                GPIO.output(Y_IN2, GPIO.LOW)
                y_pwm.ChangeDutyCycle(0)

            # 放線/放爪 控制邏輯
            if GPIO.input(BTN_ACTION) == GPIO.LOW:
                if not action_triggered:
                    print("🧵 放線中...")
                    lower_hook()
                    time.sleep(1)

                    print("🤖 收爪")
                    close_claw()
                    time.sleep(1)

                    print("🔄 收線")
                    raise_hook()
                    action_triggered = True

                elif not claw_opened:
                    print("🧸 放下物品")
                    open_claw()
                    claw_opened = True

            time.sleep(0.01)

        print("⏰ 時間到！")
        stop_motors()
        if not claw_opened:
            print("🧸 自動放爪")
            open_claw()

finally:
    x_pwm.stop()
    y_pwm.stop()
    claw_pwm.stop()
    z_pwm.stop()
    buzz_pwm.stop()
    GPIO.cleanup()
