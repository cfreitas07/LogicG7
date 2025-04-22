from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QGroupBox, QRadioButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class LogicControllerWindow(QWidget):
    def __init__(self, usb_device, parent=None):
        super().__init__(parent)
        self.usb_device = usb_device
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Logic Controller")
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create a group box for logic gate selection
        gate_group = QGroupBox("Select Logic Gate")
        gate_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        gate_layout = QVBoxLayout()

        # Create radio buttons for AND/OR selection
        self.and_radio = QRadioButton("AND Gate")
        self.or_radio = QRadioButton("OR Gate")
        self.and_radio.setChecked(True)  # Default to AND

        # Set font for radio buttons
        font = QFont("Arial", 10)
        self.and_radio.setFont(font)
        self.or_radio.setFont(font)

        # Connect radio buttons to handler
        self.and_radio.toggled.connect(self.on_gate_selection_changed)
        self.or_radio.toggled.connect(self.on_gate_selection_changed)

        # Add radio buttons to layout
        gate_layout.addWidget(self.and_radio)
        gate_layout.addWidget(self.or_radio)
        gate_group.setLayout(gate_layout)

        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: #666666;")

        # Add widgets to main layout
        layout.addWidget(gate_group)
        layout.addWidget(self.status_label)
        layout.addStretch()

    def on_gate_selection_changed(self):
        if not self.usb_device.is_connected():
            self.status_label.setText("Status: Not connected to device")
            self.status_label.setStyleSheet("color: #FF0000;")
            return

        if self.and_radio.isChecked():
            if self.usb_device.send_data(b'A'):
                self.status_label.setText("Status: AND gate selected")
                self.status_label.setStyleSheet("color: #008000;")
            else:
                self.status_label.setText("Status: Failed to send AND command")
                self.status_label.setStyleSheet("color: #FF0000;")
        else:
            if self.usb_device.send_data(b'O'):
                self.status_label.setText("Status: OR gate selected")
                self.status_label.setStyleSheet("color: #008000;")
            else:
                self.status_label.setText("Status: Failed to send OR command")
                self.status_label.setStyleSheet("color: #FF0000;") 