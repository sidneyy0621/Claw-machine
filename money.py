import RPi.GPIO as GPIO
import time

# 設定感測器訊號腳位
SENSOR_PIN = 17  # GPIO17（Pin 11）

# 初始化 GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

print("等待投幣中...")

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:  # 或 GPIO.HIGH 依據模組而定
            print("✅ 投幣成功，啟動娃娃機！")
            
            # 執行啟動動作（例如伺服馬達開啟、倒數、遊戲開始等）
            # 這裡簡單模擬 5 秒的遊戲時間
            print("🎮 娃娃機開始運作...")
            time.sleep(5)
            print("⏹ 娃娃機遊戲結束，等待下一次投幣")

            # 等待硬幣離開（防止重複觸發）
            while GPIO.input(SENSOR_PIN) == GPIO.LOW:
                time.sleep(0.1)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n程式結束")
finally:
    GPIO.cleanup()
