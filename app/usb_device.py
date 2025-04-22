import serial
import serial.tools.list_ports
from typing import Optional, List, Dict

class USBDevice:
    """Class to handle USB device connections."""
    
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.connected = False
        self.port_name = ""
        self.baud_rate = 9600  # Default baud rate
        
    def list_available_ports(self) -> List[Dict[str, str]]:
        """List all available USB ports.
        
        Returns:
            List of dictionaries containing port information
        """
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append({
                'device': port.device,
                'description': port.description,
                'manufacturer': port.manufacturer
            })
        return ports
    
    def connect(self, port_name: str, baud_rate: int = 9600) -> bool:
        """Connect to a USB device.
        
        Args:
            port_name: Name of the port to connect to
            baud_rate: Baud rate for communication
            
        Returns:
            bool: True if connection successful, False otherwise
        """
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
        """Disconnect from the USB device."""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.connected = False
        self.port_name = ""
    
    def send_data(self, data: str) -> bool:
        """Send data to the connected device.
        
        Args:
            data: String data to send
            
        Returns:
            bool: True if data sent successfully, False otherwise
        """
        if not self.connected or not self.serial_port:
            return False
        
        try:
            self.serial_port.write(data.encode())
            return True
        except serial.SerialException:
            return False
    
    def read_data(self, size: int = 1024) -> Optional[str]:
        """Read data from the connected device.
        
        Args:
            size: Number of bytes to read
            
        Returns:
            str: Received data or None if error
        """
        if not self.connected or not self.serial_port:
            return None
        
        try:
            data = self.serial_port.read(size)
            return data.decode('utf-8')
        except serial.SerialException:
            return None
    
    def is_connected(self) -> bool:
        """Check if device is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.connected and self.serial_port and self.serial_port.is_open 