import RPi.GPIO as GPIO
import time

# 馬達控制腳位
X_IN1, X_IN2, X_EN = 17, 27, 18
Y_IN1, Y_IN2, Y_EN = 22, 23, 24

# 按鈕腳位
BTN_UP = 5
BTN_DOWN = 6
BTN_LEFT = 13
BTN_RIGHT = 19

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 設定腳位
for pin in [X_IN1, X_IN2, X_EN, Y_IN1, Y_IN2, Y_EN]:
    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(BTN_UP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BTN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BTN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 初始化 PWM
x_pwm = GPIO.PWM(X_EN, 1000)
y_pwm = GPIO.PWM(Y_EN, 1000)
x_pwm.start(0)
y_pwm.start(0)

def stop_motors():
    GPIO.output(X_IN1, GPIO.LOW)
    GPIO.output(X_IN2, GPIO.LOW)
    x_pwm.ChangeDutyCycle(0)

    GPIO.output(Y_IN1, GPIO.LOW)
    GPIO.output(Y_IN2, GPIO.LOW)
    y_pwm.ChangeDutyCycle(0)

def return_to_origin():
    print("⏱ 時間到！返回原點...")
    GPIO.output(X_IN1, GPIO.HIGH)
    GPIO.output(X_IN2, GPIO.LOW)
    GPIO.output(Y_IN1, GPIO.HIGH)
    GPIO.output(Y_IN2, GPIO.LOW)
    x_pwm.ChangeDutyCycle(100)
    y_pwm.ChangeDutyCycle(100)
    time.sleep(2)
    stop_motors()
    print("✅ 已回到原點")

try:
    print("🎮 遊戲開始！（限時 25 秒）")
    start_time = time.time()

    while time.time() - start_time < 25:
        # X 軸控制（按下才動）
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

        # Y 軸控制（按下才動）
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

        time.sleep(0.01)

    stop_motors()
    return_to_origin()

finally:
    x_pwm.stop()
    y_pwm.stop()
    GPIO.cleanup()
