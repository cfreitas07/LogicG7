# PIC LED Control via UART

This project demonstrates how to control an LED on a PIC microcontroller using Python through UART communication.

## Hardware Requirements

- PIC Microcontroller (configured with UART)
- LED connected to RC6 pin
- USB to UART converter (if needed)

## Software Requirements

- Python 3.x
- PySerial library
- MPLAB X IDE (for PIC programming)
- MCC (MPLAB Code Configurator)

## Configuration

### PIC Configuration
- UART Baud Rate: 9600
- LED Pin: RC6
- Command to toggle LED: 0xA1
- Response after toggle: 'O'

### Python Configuration
```python
PORT = 'COM4'      # Change this if your port is different
BAUDRATE = 9600
TOGGLE_COMMAND = 0xA1
EXPECTED_RESPONSE = b'O'
BLINK_COUNT = 10
DELAY_BETWEEN_BLINKS = 1  # seconds
```

## Usage

1. Flash the PIC code to your microcontroller
2. Connect the PIC to your computer via UART
3. Run the Python script:
   ```bash
   python testLED.py
   ```

## Communication Protocol

1. PIC sends 'R' when ready
2. Python sends 0xA1 to toggle LED
3. PIC responds with 'O' after successful toggle

## Troubleshooting

- Verify the correct COM port in Device Manager
- Ensure baud rate matches on both PIC and Python (9600)
- Check LED connections to RC6 pin
- Verify UART connections (TX/RX) 