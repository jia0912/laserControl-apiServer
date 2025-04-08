import requests
import time

# 定義 API 的基礎 URL
BASE_URL = "http://localhost:5000"

def test_send_command(command):
    """
    測試 /send_command 接口，傳送指令到伺服器
    :param command: 要發送的指令 (1, 2, 3)
    """
    url = f"{BASE_URL}/send_command"
    payload = {"command": command}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ 成功: {response.json()}")
        else:
            print(f"⚠️ 錯誤: {response.json()}")
    except Exception as e:
        print(f"❌ 發送失敗: {e}")

if __name__ == "__main__":
    # 測試有效的指令
    print("Testing valid commands...")
    while(1):
        test_send_command(1)  # 測試指令 1
        test_send_command(2)  # 測試指令 2
        test_send_command(3)  # 測試指令 3

    # 測試無效的指令
    print("\nTesting invalid commands...")
    test_send_command(4)  # 測試無效指令
    test_send_command("invalid")  # 測試非數字指令

    print("\nend....")
    test_send_command(0)  
