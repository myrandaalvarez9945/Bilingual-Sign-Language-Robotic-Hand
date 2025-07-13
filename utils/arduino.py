# utils/arduino.py

def send_to_arduino(message):
    try:
        import serial
        import time

        SERIAL_PORT = "COM3"  # 👈 Replace with your actual Arduino port
        BAUD_RATE = 9600

        print(f"[Arduino] Connecting on {SERIAL_PORT} at {BAUD_RATE}...")
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            time.sleep(2)  # Give Arduino time to reset
            print(f"[Arduino] Sending message: {message}")
            ser.write(message.encode())
            print("[Arduino] Message sent successfully.")
    except serial.SerialException as e:
        print(f"[ERROR] Serial communication failed: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")