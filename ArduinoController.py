import serial
import serial.tools.list_ports
import json
import os
import time

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

        if port:
            self.config["port"] = port
            save_config(self.config)

        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def list_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

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
            self.serial_conn = serial.Serial(
                port,
                self.config.get("baudrate", 115200),
                timeout=1
            )
            print(f"Connected to Arduino on {port}")
            time.sleep(1)  #**key**--wait Arduino init
        except Exception as e:
            print(f"Failed to connect to Arduino: {e}")

    def send_command(self, command: int, wait_for='N', timeout=5):
        self.config = load_config()
        commands = self.config.get("commands", {})

        if str(command) not in commands:
            raise ValueError(f"Invalid command. Allowed: {list(commands.keys())}")

        ctrl_code = commands[str(command)]
        try:
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(f"{ctrl_code}\n".encode())
            print(f"<{command}> {ctrl_code} sent to Arduino. Waiting for response...")

            start_time = time.time()
            response = ""
            while time.time() - start_time < timeout:
                if self.serial_conn.in_waiting:
                    response += self.serial_conn.read(self.serial_conn.in_waiting).decode()
                    if wait_for in response:
                        print(f"Arduino response received: {wait_for}")
                        return
                time.sleep(0.1)

            raise TimeoutError("Timeout waiting for Arduino response.")

        except Exception as e:
            raise Exception(f"Failed to send command to Arduino: {e}")

    def close(self):
        if self.serial_conn and self.serial_conn.is_open:
            # try:
            #     self.send_command(0)  # 重設 Arduino 狀態
            # except Exception as e:
            #     print("laserError：", e)
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
        except KeyboardInterrupt:
            arduino.send_command(0)
            arduino.close()
        except Exception as e:
            print("laserError：", e)
    arduino.close()

    # --for MOST--
    # 結束時傳個0關雷射
    # from ArduinoController import ArduinoController

    # with ArduinoController() as laser:
    #     laser.send_command(0) # command (0, 1, 2, 3)