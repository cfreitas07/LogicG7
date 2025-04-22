import serial
import serial.tools.list_ports
from typing import Optional, List, Dict

class USBDevice:
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.connected = False
        self.port_name = ""
        self.baud_rate = 9600

    def list_available_ports(self) -> List[Dict[str, str]]:
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'description': port.description,
                'manufacturer': port.manufacturer
            })
        return ports

    def connect(self, port_name: str, baud_rate: int = 9600) -> bool:
        try:
            self.serial_port = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                timeout=1
            )
            self.connected = True
            self.port_name = port_name
            self.baud_rate = baud_rate
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {port_name}: {str(e)}")
            self.connected = False
            return False

    def disconnect(self) -> None:
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.connected = False
        self.port_name = ""

    def send_data(self, data: bytes) -> bool:
        if not self.connected or not self.serial_port:
            return False
        try:
            self.serial_port.write(data)
            return True
        except serial.SerialException:
            return False

    def read_data(self, size: int = 1) -> Optional[bytes]:
        if not self.connected or not self.serial_port:
            return None
        try:
            return self.serial_port.read(size)
        except serial.SerialException:
            return None

    def is_connected(self) -> bool:
        return self.connected and self.serial_port and self.serial_port.is_open 