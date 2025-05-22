import pigpio
import time

pi = pigpio.pi()
servo_pin = 17  # 改成你實際接的腳位

if not pi.connected:
    print("請先執行：sudo pigpiod")
    exit()

try:
    print("移動到中間（90 度）")
    pi.set_servo_pulsewidth(servo_pin, 1500)
    time.sleep(1)

    print("左轉 60 度（到 30 度位置）")
    pi.set_servo_pulsewidth(servo_pin, 900)  # 30 度
    time.sleep(10)

    print("回到中間（90 度）")
    pi.set_servo_pulsewidth(servo_pin, 1500)
    time.sleep(1)

    print("停止伺服輸出")
    pi.set_servo_pulsewidth(servo_pin, 0)

except KeyboardInterrupt:
    pi.set_servo_pulsewidth(servo_pin, 0)

finally:
    pi.stop()
