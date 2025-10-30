class RFSerialManager:
    def __init__(self, rf_freq, serial_port, baudrate, unlock_code):
        self.rf_freq = rf_freq
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.unlock_code = unlock_code
        self.rf_active = False
        self.unlocked = False
        self.serial_conn = None
        self.received_data = []

    def initialize_rf(self):
        # 检查射频芯片参数是否一致
        print(f"Initializing RF chip at {self.rf_freq} Hz")
        # 这里实际应检测射频模块频率
        self.rf_active = True  # 假定射频检测通过

    def open_serial(self):
        import serial
        self.serial_conn = serial.Serial(self.serial_port, self.baudrate)
        print(f"Serial port {self.serial_port} opened at {self.baudrate} baud")

    def verify_unlock(self, code, file_data):
        if self.rf_active and code == self.unlock_code and file_data:
            self.unlocked = True
            print("Unlocked: RF and password verified, file exists.")
        else:
            self.unlocked = False
            print("Unlock failed.")

    def send_data(self, data):
        if self.unlocked and self.rf_active:
            # 发送二进制数据
            self.serial_conn.write(data)
            print("Data sent via RF serial.")
        else:
            print("Cannot send: Not unlocked or RF inactive.")

    def receive_data(self):
        if self.unlocked and self.rf_active:
            data = self.serial_conn.read(1024)  # 假定最大读取1024字节
            self.received_data.append(data)
            print("Received data:", data)
            return data
        else:
            print("Cannot receive: Not unlocked or RF inactive.")

    def rf_lost(self):
        # 射频不在时，只能保存串口密码和记录
        self.rf_active = False
        print("RF lost. Only password and record remain via serial.")

# 用法示例
if __name__ == "__main__":
    manager = RFSerialManager(rf_freq=89909, serial_port='/dev/ttyS0', baudrate=115200, unlock_code=10026)
    manager.initialize_rf()
    manager.open_serial()
    # 验证解锁（假定 file_data 为 b'binary_data'）
    manager.verify_unlock(10026, b'binary_data')
    manager.send_data(b'\x01\x02\x03\x04')
    manager.receive_data()
    manager.rf_lost()