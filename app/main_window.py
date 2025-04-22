from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QComboBox,
                             QMenuBar, QMenu, QStatusBar, QMdiArea, QMdiSubWindow,
                             QFrame, QGroupBox, QGridLayout)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPalette, QColor, QAction, QFont

from .usb_device import USBDevice
from .pic_controller import PICController

class StatusLED(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(16, 16)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self._connected = False
        self.update_color()

    def set_connected(self, connected: bool):
        self._connected = connected
        self.update_color()

    def update_color(self):
        palette = self.palette()
        color = QColor("#00FF00") if self._connected else QColor("#FF0000")
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.usb_device = USBDevice()
        self.pic_controller = PICController(self.usb_device)
        self.mdi_windows = {}  # Store references to open windows
        self._init_ui()
        self._create_menu_bar()
        self._create_status_bar()

    def _create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Logic Gate Menu
        logic_menu = menubar.addMenu('Logic Gate')
        # Empty for now
        
        # Window Menu
        window_menu = menubar.addMenu('Window')
        tile_action = QAction('Tile', self)
        tile_action.triggered.connect(self.mdi_area.tileSubWindows)
        cascade_action = QAction('Cascade', self)
        cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)
        window_menu.addAction(tile_action)
        window_menu.addAction(cascade_action)

    def _create_status_bar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create status LED
        self.status_led = StatusLED()
        self.statusBar.addPermanentWidget(self.status_led)
        
        # Create status label
        self.status_label = QLabel("Not Connected")
        self.statusBar.addPermanentWidget(self.status_label)
        
        self.statusBar.showMessage("Ready")

    def _init_ui(self):
        self.setWindowTitle("PIC Logic Gate Controller")
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Serial Communication Group
        serial_group = QGroupBox("Serial Communication")
        serial_group.setStyleSheet("""
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
        serial_layout = QGridLayout()
        serial_layout.setSpacing(10)
        
        # Port Selection
        port_label = QLabel("Port:")
        port_label.setFont(QFont("Arial", 10))
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(300)
        self.port_combo.setFont(QFont("Arial", 10))
        
        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setFont(QFont("Arial", 10))
        self.connect_button.setMinimumWidth(100)
        self.connect_button.clicked.connect(self.toggle_connection)
        
        # Status Label
        self.conn_status_label = QLabel("Not Connected")
        self.conn_status_label.setFont(QFont("Arial", 10))
        self.conn_status_label.setStyleSheet("color: #666666;")
        
        # Test Communication Button
        self.test_button = QPushButton("Test Communication")
        self.test_button.setFont(QFont("Arial", 10))
        self.test_button.setMinimumWidth(150)
        self.test_button.setEnabled(False)
        self.test_button.clicked.connect(self.test_communication)
        
        # Result Label
        self.result_label = QLabel("Status: N/A")
        self.result_label.setFont(QFont("Arial", 10))
        self.result_label.setStyleSheet("color: #666666;")
        
        # Add widgets to grid layout
        serial_layout.addWidget(port_label, 0, 0)
        serial_layout.addWidget(self.port_combo, 0, 1)
        serial_layout.addWidget(self.connect_button, 0, 2)
        serial_layout.addWidget(self.conn_status_label, 0, 3)
        serial_layout.addWidget(self.test_button, 1, 1)
        serial_layout.addWidget(self.result_label, 1, 2, 1, 2)
        
        serial_group.setLayout(serial_layout)
        
        # Add serial group to main layout
        main_layout.addWidget(serial_group)
        
        # Create MDI Area for other windows
        self.mdi_area = QMdiArea()
        main_layout.addWidget(self.mdi_area)
        
        # Refresh ports
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
            self.conn_status_label.setText("Not Connected")
            self.test_button.setEnabled(False)
            self.update_connection_status(False, "")
        else:
            if self.port_combo.count() == 0:
                return
            port_name = self.port_combo.currentData()
            if self.usb_device.connect(port_name):
                self.connect_button.setText("Disconnect")
                self.conn_status_label.setText(f"Connected to {port_name}")
                self.test_button.setEnabled(True)
                self.update_connection_status(True, port_name)

                # Wait for optional startup byte from PIC
                self.usb_device.read_data(1)  # Clear buffer

    def test_communication(self):
        result = self.pic_controller.toggle_led()
        if result:
            self.result_label.setText("Status: ✅ Communication Successful")
            self.result_label.setStyleSheet("color: #008000;")
        else:
            self.result_label.setText("Status: ❌ Communication Failed")
            self.result_label.setStyleSheet("color: #FF0000;")

    def update_connection_status(self, connected: bool, port_name: str = ""):
        self.status_led.set_connected(connected)
        if connected:
            self.status_label.setText(f"Connected to {port_name}")
        else:
            self.status_label.setText("Not Connected")

    def closeEvent(self, event):
        # Clean up resources before closing
        if self.usb_device.is_connected():
            self.usb_device.disconnect()
        event.accept() 