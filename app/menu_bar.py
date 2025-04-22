from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal

from app.usb_device import USBDevice
from app.led_indicator import LEDIndicator

class DeviceMenuWidget(QWidget):
    """Widget for device connection controls in the menu bar."""
    
    connection_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.usb_device = USBDevice()
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the user interface."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Port selection
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(200)
        
        # Connection button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setFixedWidth(100)
        self.connect_button.clicked.connect(self.toggle_connection)
        
        # Status label and LED
        status_layout = QHBoxLayout()
        self.led_indicator = LEDIndicator()
        self.status_label = QLabel("Not Connected")
        self.status_label.setFixedWidth(150)
        status_layout.addWidget(self.led_indicator)
        status_layout.addWidget(self.status_label)
        status_layout.setSpacing(5)
        
        # Add widgets to layout
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_combo)
        layout.addWidget(self.connect_button)
        layout.addLayout(status_layout)
        layout.addStretch()
        
        # Initial port refresh
        self.refresh_ports()
        
    def refresh_ports(self):
        """Refresh the list of available ports."""
        self.port_combo.clear()
        ports = self.usb_device.list_available_ports()
        
        for port in ports:
            display_text = f"{port['device']} - {port['description']}"
            self.port_combo.addItem(display_text, port['device'])
            
    def toggle_connection(self):
        """Toggle the connection to the selected port."""
        if self.usb_device.is_connected():
            self.usb_device.disconnect()
            self.connect_button.setText("Connect")
            self.status_label.setText("Not Connected")
            self.led_indicator.set_state(False)
            self.connection_changed.emit(False)
        else:
            if self.port_combo.count() == 0:
                return
                
            port_name = self.port_combo.currentData()
            if self.usb_device.connect(port_name):
                self.connect_button.setText("Disconnect")
                self.status_label.setText(f"Connected to {port_name}")
                self.led_indicator.set_state(True)
                self.connection_changed.emit(True)
                
    def get_device(self) -> USBDevice:
        """Get the USB device instance."""
        return self.usb_device

def create_menu_bar(parent):
    """Create and return the application's menu bar.
    
    Args:
        parent: The parent widget for the menu bar.
        
    Returns:
        QMenuBar: The configured menu bar.
    """
    menubar = QMenuBar(parent)
    
    # File menu
    file_menu = menubar.addMenu("File")
    file_menu.addAction("New")
    file_menu.addAction("Open")
    file_menu.addAction("Save")
    file_menu.addSeparator()
    file_menu.addAction("Exit")
    
    # Edit menu
    edit_menu = menubar.addMenu("Edit")
    edit_menu.addAction("Cut")
    edit_menu.addAction("Copy")
    edit_menu.addAction("Paste")
    
    # Help menu
    help_menu = menubar.addMenu("Help")
    help_menu.addAction("About")
    
    # Add device connection widget to menu bar
    device_widget = DeviceMenuWidget()
    menubar.setCornerWidget(device_widget)
    
    return menubar 