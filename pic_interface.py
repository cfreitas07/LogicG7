import sys
import serial
import serial.tools.list_ports
from typing import Optional, List, Dict
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QComboBox)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPalette, QColor

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

class PICController:
    CMD_TOGGLE_LED = 0xA1
    RESPONSE_OK = b'O'

    def __init__(self, usb_device: USBDevice):
        self.usb_device = usb_device

    def toggle_led(self) -> bool:
        if not self.usb_device.is_connected():
            return False
        success = self.usb_device.send_data(bytes([self.CMD_TOGGLE_LED]))
        if not success:
            return False

        # Try to get a response from PIC
        response = self.usb_device.read_data()
        return response == self.RESPONSE_OK

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.usb_device = USBDevice()
        self.pic_controller = PICController(self.usb_device)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("PIC LED Control")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Connection UI
        conn_layout = QHBoxLayout()
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(200)
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        self.status_label = QLabel("Not Connected")
        conn_layout.addWidget(QLabel("Port:"))
        conn_layout.addWidget(self.port_combo)
        conn_layout.addWidget(self.connect_button)
        conn_layout.addWidget(self.status_label)

        # LED Control UI
        led_layout = QHBoxLayout()
        self.led_button = QPushButton("Toggle LED")
        self.led_button.setEnabled(False)
        self.led_button.clicked.connect(self.toggle_led)
        self.result_label = QLabel("Status: N/A")
        led_layout.addWidget(self.led_button)
        led_layout.addWidget(self.result_label)

        layout.addLayout(conn_layout)
        layout.addLayout(led_layout)
        layout.addStretch()

        self.refresh_ports()

    def refresh_ports(self):
        self.port_combo.clear()
        ports = self.usb_device.list_available_ports()
        for port in ports:
            display_text = f"{port['device']} - {port['description']}"
            self.port_combo.addItem(display_text, port['device'])

    def toggle_connection(self):
        if self.usb_device.is_connected():
            self.usb_device.disconnect()
            self.connect_button.setText("Connect")
            self.status_label.setText("Not Connected")
            self.led_button.setEnabled(False)
        else:
            if self.port_combo.count() == 0:
                return
            port_name = self.port_combo.currentData()
            if self.usb_device.connect(port_name):
                self.connect_button.setText("Disconnect")
                self.status_label.setText(f"Connected to {port_name}")
                self.led_button.setEnabled(True)

                # Wait for optional startup byte from PIC
                self.usb_device.read_data(1)  # Clear buffer

    def toggle_led(self):
        result = self.pic_controller.toggle_led()
        if result:
            self.result_label.setText("Status: ✅ Toggled")
        else:
            self.result_label.setText("Status: ❌ No response")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
