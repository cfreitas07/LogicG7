from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal

from app.usb_device import USBDevice

class DeviceConnectionWidget(QWidget):
    """Widget for managing USB device connections."""
    
    # Signal emitted when connection status changes
    connection_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.usb_device = USBDevice()
        self._init_ui()
        
    def _init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Port selection
        port_layout = QHBoxLayout()
        self.port_label = QLabel("Port:")
        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_ports)
        
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_button)
        
        # Connection button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        
        # Status label
        self.status_label = QLabel("Not Connected")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Add widgets to layout
        layout.addLayout(port_layout)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.status_label)
        
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
            self.connection_changed.emit(False)
        else:
            if self.port_combo.count() == 0:
                QMessageBox.warning(self, "Error", "No ports available")
                return
                
            port_name = self.port_combo.currentData()
            if self.usb_device.connect(port_name):
                self.connect_button.setText("Disconnect")
                self.status_label.setText(f"Connected to {port_name}")
                self.connection_changed.emit(True)
            else:
                QMessageBox.warning(self, "Error", f"Failed to connect to {port_name}")
                
    def get_device(self) -> USBDevice:
        """Get the USB device instance.
        
        Returns:
            USBDevice: The USB device instance
        """
        return self.usb_device 