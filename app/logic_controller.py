from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QGroupBox, QRadioButton,
                             QFrame)
from PyQt6.QtCore import Qt, QRect, QPoint, QRectF, QSize
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush, QPainterPath, QPixmap
import os

class LogicGateWidget(QFrame):
    def __init__(self, gate_type, parent=None):
        super().__init__(parent)
        self.gate_type = gate_type  # 'AND' or 'OR'
        self.selected = False
        self.setMinimumSize(200, 150)  # Reduced minimum size
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #CCCCCC;
                border-radius: 10px;
            }
        """)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Load gate image
        image_path = os.path.join('src', 'images', f'{gate_type.lower()}.png')
        self.original_image = QPixmap(image_path)
        if self.original_image.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            # Scale image to fit widget while maintaining aspect ratio
            self.gate_image = self.original_image.scaled(
                160, 120,  # Target size
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the gate image centered
        if hasattr(self, 'gate_image') and not self.gate_image.isNull():
            # Calculate the position to center the image
            x = (self.width() - self.gate_image.width()) // 2
            y = (self.height() - self.gate_image.height()) // 2
            painter.drawPixmap(x, y, self.gate_image)

        # Draw selection highlight if selected
        if self.selected:
            painter.setPen(QPen(QColor("#0078D7"), 3))
            painter.drawRect(self.rect().adjusted(2, 2, -2, -2))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'original_image') and not self.original_image.isNull():
            # Scale image to fit new size while maintaining aspect ratio
            target_width = min(self.width() - 40, 160)  # Leave some padding
            target_height = min(self.height() - 30, 120)  # Leave some padding
            self.gate_image = self.original_image.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

    def mousePressEvent(self, event):
        self.selected = True
        self.update()
        if self.gate_type == 'AND':
            self.parent().select_and_gate()
        else:
            self.parent().select_or_gate()

class LogicControllerWindow(QWidget):
    def __init__(self, usb_device, parent=None):
        super().__init__(parent)
        self.usb_device = usb_device
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Logic Controller")
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create title label
        title_label = QLabel("Logic Gate Selection")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Create gates container
        gates_layout = QHBoxLayout()
        gates_layout.setSpacing(40)

        # Create AND gate widget
        self.and_gate = LogicGateWidget('AND', self)
        self.and_gate.selected = True  # Default selection
        gates_layout.addWidget(self.and_gate)

        # Create OR gate widget
        self.or_gate = LogicGateWidget('OR', self)
        gates_layout.addWidget(self.or_gate)

        layout.addLayout(gates_layout)

        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: #666666;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Add some spacing at the bottom
        layout.addStretch()

    def select_and_gate(self):
        self.and_gate.selected = True
        self.or_gate.selected = False
        self.and_gate.update()
        self.or_gate.update()
        self._send_gate_command('A')

    def select_or_gate(self):
        self.and_gate.selected = False
        self.or_gate.selected = True
        self.and_gate.update()
        self.or_gate.update()
        self._send_gate_command('O')

    def _send_gate_command(self, command):
        if not self.usb_device.is_connected():
            self.status_label.setText("Status: Not connected to device")
            self.status_label.setStyleSheet("color: #FF0000;")
            return

        if self.usb_device.send_data(command.encode()):
            self.status_label.setText(f"Status: Sending {command} command...")
            self.status_label.setStyleSheet("color: #666666;")
        else:
            self.status_label.setText("Status: Failed to send command")
            self.status_label.setStyleSheet("color: #FF0000;") 