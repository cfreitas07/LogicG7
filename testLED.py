import serial
import time

PORT = 'COM4'      # Change this if your port is different
BAUDRATE = 9600
TOGGLE_COMMAND = 0xA1
EXPECTED_RESPONSE = b'O'
BLINK_COUNT = 10
DELAY_BETWEEN_BLINKS = 1  # seconds

def main():
    try:
        print(f"Connecting to {PORT} at {BAUDRATE} baud...")
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        time.sleep(2)  # Let the PIC initialize

        # Wait for PIC startup message
        print("Waiting for PIC 'Ready' signal (R)...")
        if ser.in_waiting:
            ready = ser.read()
            if ready == b'R':
                print("PIC is ready!")
            else:
                print(f"Unexpected startup message: {ready}")

        print(f"Starting {BLINK_COUNT} LED toggles...")
        for i in range(BLINK_COUNT):
            print(f"Sending toggle command {i + 1}...")
            ser.write(bytes([TOGGLE_COMMAND]))

            time.sleep(0.1)  # Short delay before reading

            if ser.in_waiting:
                response = ser.read()
                if response == EXPECTED_RESPONSE:
                    print(f"✅ LED toggled (response: {response})")
                else:
                    print(f"⚠️ Unexpected response: {response}")
            else:
                print("❌ No response received from PIC")

            time.sleep(DELAY_BETWEEN_BLINKS)

        print("Test complete.")
        ser.close()

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"General error: {e}")

if __name__ == '__main__':
    main()
