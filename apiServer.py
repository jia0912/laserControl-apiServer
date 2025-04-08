from flask import Flask, request
from ArduinoController import ArduinoController  # 確保檔名與 class 名稱一致

app = Flask(__name__)

# 初始化 Arduino 控制器
arduino = ArduinoController()

@app.route('/send_command', methods=['POST', 'GET'])
def send_command():
    try:
        # 允許用 GET 或 POST 傳指令，GET 用 URL 參數，POST 可用 form-data 或 JSON
        command = request.args.get("command") or request.form.get("command") or request.json.get("command")
        
        if command is None:
            return {"status": "error", "message": "No command provided."}, 400

        arduino.send_command(int(command))  # 傳送指令到 Arduino
        return {"status": "success", "message": f"Command {command} sent to laserCtrl."}, 200

    except ValueError as ve:
        return {"status": "error", "message": str(ve)}, 400
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        arduino.close()
