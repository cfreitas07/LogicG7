from typing import Optional
from .usb_device import USBDevice

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