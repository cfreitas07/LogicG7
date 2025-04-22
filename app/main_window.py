from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QComboBox,
                             QMenuBar, QMenu, QStatusBar, QMdiArea, QMdiSubWindow)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPalette, QColor, QAction

from .usb_device import USBDevice
from .pic_controller import PICController

class SerialWindow(QWidget):
    def __init__(self, usb_device: USBDevice, pic_controller: PICController, parent=None):
        super().__init__(parent)
        self.usb_device = usb_device
        self.pic_controller = pic_controller
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Serial Communication")
        layout = QVBoxLayout(self)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.usb_device = USBDevice()
        self.pic_controller = PICController(self.usb_device)
        self.mdi_windows = {}  # Store references to open windows
        self._init_ui()
        self._create_menu_bar()

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
        
        # Hardware Menu
        hardware_menu = menubar.addMenu('Hardware')
        serial_action = QAction('Serial Communication', self)
        serial_action.triggered.connect(self.show_serial_window)
        hardware_menu.addAction(serial_action)

        # Window Menu
        window_menu = menubar.addMenu('Window')
        tile_action = QAction('Tile', self)
        tile_action.triggered.connect(self.mdi_area.tileSubWindows)
        cascade_action = QAction('Cascade', self)
        cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)
        window_menu.addAction(tile_action)
        window_menu.addAction(cascade_action)

    def _init_ui(self):
        self.setWindowTitle("PIC Logic Gate Controller")
        self.setGeometry(100, 100, 1200, 800)

        # Create MDI Area
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

    def show_serial_window(self):
        # Check if window already exists
        if 'serial' in self.mdi_windows and not self.mdi_windows['serial'].isHidden():
            self.mdi_windows['serial'].showNormal()
            self.mdi_windows['serial'].widget().raise_()
            return

        # Create new serial window
        sub_window = QMdiSubWindow()
        serial_widget = SerialWindow(self.usb_device, self.pic_controller)
        sub_window.setWidget(serial_widget)
        sub_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()
        
        # Store reference to the window
        self.mdi_windows['serial'] = sub_window

    def closeEvent(self, event):
        # Clean up resources before closing
        if self.usb_device.is_connected():
            self.usb_device.disconnect()
        event.accept() 