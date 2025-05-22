import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.OUT)

p1 = GPIO.PWM(21, 440)
p1.start(0)  # duty cycle 0 表示靜音

sheets = [
    # 🎶 Do, a deer, a female deer
    261.63, 0, 293.66, 329.63, 329.63, 0,
    261.63, 329.63, 0, 261.63, 0, 329.63,
    0, 0, 293.66, 0, 329.63, 349.23, 349.23,
    329.63, 293.66, 349.23, 0,

    # 🎶 Re, a drop of golden sun
    261.63, 392.00, 392.00, 440.00, 392.00, 349.23,
    329.63, 261.63, 293.66, 329.63, 261.63, 261.63,

    # 🎶 Mi, a name I call myself
    392.00, 392.00, 440.00, 392.00, 349.23, 329.63,
    261.63, 0, 293.66, 293.66, 329.63, 349.23,
    392.00, 0,

    # 🎶 Fa, a long long way to run
    392.00, 440.00, 440.00, 493.88, 440.00, 392.00,
    349.23, 293.66, 349.23, 392.00, 329.63, 0,

    # 🎶 So, a needle pulling thread
    392.00, 440.00, 493.88, 523.25, 493.88, 440.00,
    392.00, 349.23, 392.00, 440.00, 392.00, 0,

    # 🎶 La, a note to follow so
    440.00, 493.88, 523.25, 587.33, 523.25, 493.88,
    440.00, 392.00, 440.00, 493.88, 440.00, 0,

    # 🎶 Ti, a drink with jam and bread
    493.88, 523.25, 587.33, 659.25, 587.33, 523.25,
    493.88, 440.00, 493.88, 523.25, 493.88, 0,

    # 🎶 That will bring us back to Do
    523.25, 587.33, 659.25, 698.46, 659.25, 587.33,
    523.25, 493.88, 523.25, 587.33, 523.25, 0
]


# 播放 5 次
for _ in range(2):
    for s in sheets:
        if s == 0:
            p1.ChangeDutyCycle(0)
        else:
            p1.ChangeFrequency(s)
            p1.ChangeDutyCycle(50)
        time.sleep(0.25)        # 音符長度
        p1.ChangeDutyCycle(0)
        time.sleep(0.05)        # 音符間隔

p1.stop()
GPIO.cleanup()
