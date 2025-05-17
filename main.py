import time
import coin_detector
import claw_controller
import motor_x_controller
import motor_y_controller

def on_coin_inserted(channel):
    """
    當偵測到投幣事件時呼叫的函式。
    """
    print("偵測到投幣！開始遊戲流程。")
    start_game()

def start_game():
    """
    遊戲流程：控制爪子移動、抓取物品、返回初始位置。
    """
    try:
        # 啟用搖桿控制（模擬玩家控制爪子移動）
        print("玩家控制爪子移動中...")
        time.sleep(5)  # 模擬控制時間

        # 抓取物品
        print("開始抓取物品...")
        claw_controller.grab_sequence(None)

        # 返回初始位置
        print("爪子返回初始位置...")
        motor_x_controller.stop()
        motor_y_controller.stop()
        print("系統重置完成，等待下一次投幣。")
    except Exception as e:
        print(f"遊戲流程中發生錯誤: {e}")

def main():
    try:
        # 初始化投幣偵測器，並設定回呼函式
        coin_detector.setup_coin_detector(on_coin_inserted)
        print("等待投幣中...")

        # 主迴圈
        while True:
            time.sleep(1)  # 保持程式運行
    except KeyboardInterrupt:
        print("程式中止。")
    finally:
        # 清除 GPIO 設定
        coin_detector.cleanup()

if __name__ == "__main__":
    main()