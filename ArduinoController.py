import serial
import serial.tools.list_ports
import json
import os

# 設定檔路徑
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "port": "COM9",
            "baudrate": 115200,
            "commands": {
                "0": "00",
                "1": "11160034450090",
                "2": "11107235250090",
                "3": "11198934420090"
            }
        }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

class ArduinoController:
    def __init__(self, port=None):
        self.config = load_config()
        self.serial_conn = None

        # 如果初始化時有提供 port，就用它，否則用 config.json 的 port
        if port:
            self.config["port"] = port
            save_config(self.config)  # 儲存新的 port

        self.connect()


    def list_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

    def connect(self):
        available_ports = self.list_ports()
        if not available_ports:
            print("No available COM ports found.")
            return
        
        port = self.config.get("port")
        if port not in available_ports:
            print("Configured port not found. Available ports:", available_ports)
            port = input("Enter the COM port to use: ")
            self.config["port"] = port
            save_config(self.config)

        try:
            self.serial_conn = serial.Serial(port, self.config.get("baudrate", 115200), timeout=1)
            print(f"Connected to Arduino on {port}")
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")

    def send_command(self, command: int):
        self.config = load_config()  # 每次發送指令時重新載入設定檔
        commands = self.config.get("commands", {})
        if str(command) not in commands:
            raise ValueError(f"Invalid command. Allowed: {list(commands.keys())}")
        try:
            ctrl_code = commands[str(command)]
            self.serial_conn.write(f"{ctrl_code}\n".encode())
            print(f"Command {ctrl_code} sent to Arduino.")
        except Exception as e:
            raise Exception(f"Failed to send command to Arduino: {e}")

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            arduino.send_command(int("0"))
            self.serial_conn.close()
            print("Connection to Arduino closed.")

if __name__ == '__main__':
    arduino = ArduinoController()
    while True:
        command = input("Enter command (0, 1, 2, 3) or 'exit': ")
        if command.lower() == 'exit':
            break
        try:
            arduino.send_command(int(command))
        except ValueError as e:
            print(e)
    arduino.close()