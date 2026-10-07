# AEROSAR MAVLink Connection Baseline

This provides the simplest reliable foundation for connecting a Raspberry Pi 5 to a SpeedyBee Flight Controller running ArduPilot via UART/Serial.

## Architecture
Raspberry Pi 5 → UART → MAVLink (pymavlink) → ArduPilot

## Setup

1. **Install Dependencies**
   It is recommended to use a virtual environment or install dependencies via pip:
   ```bash
   pip install -r requirements.txt
   ```

2. **Hardware Checks Required**
   - Ensure the flight controller is powered on (usually via USB or battery).
   - Ensure the TX pin of the flight controller is connected to the RX pin of the Raspberry Pi.
   - Ensure the RX pin of the flight controller is connected to the TX pin of the Raspberry Pi.
   - Ensure the GND of the flight controller is connected to the GND of the Raspberry Pi.
   - Identify your Raspberry Pi serial port. By default, `/dev/serial0` points to the primary UART. You might need to enable the serial port in `raspi-config`.

3. **Configuration**
   Edit `vehicle_mavlink/config.py` and modify the following values to match your setup:
   - `SERIAL_PORT`: The serial port your FC is connected to (e.g., `'/dev/serial0'`, `'/dev/ttyAMA0'`).
   - `BAUD_RATE`: The baud rate (usually `57600` for telemetry).
   
   If you just want to test the software without physical hardware, set `TEST_MODE = True`.

## Running the Service

```bash
cd vehicle_mavlink
python main.py
```

## Expected Output

### When FC is connected successfully:
```text
=======================================
 AEROSAR MAVLink Telemetry Service
=======================================
[INFO] Attempting to open serial connection on /dev/serial0 at 57600 baud...
[INFO] Serial connection opened successfully.
[INFO] Waiting for ArduPilot heartbeat...
[INFO] Heartbeat received.
[INFO] System ID: 1
[INFO] Component ID: 1
[INFO] MAVLink connection established.
[INFO] Starting telemetry loop. Press Ctrl+C to stop.
HEARTBEAT | Mode: 0, Armed: False
SYSTEM    | Battery: 12.40V, 95%
POSITION  | Lat: 37.774900, Lon: -122.419400, Alt: 10.00m
ATTITUDE  | Roll: 0.10, Pitch: -0.05, Yaw: 1.50
```

### When FC is not connected (or wrong port/baud):
```text
=======================================
 AEROSAR MAVLink Telemetry Service
=======================================
[INFO] Attempting to open serial connection on /dev/serial0 at 57600 baud...
[ERROR] Serial connection failed: [Errno 2] could not open port /dev/serial0: [Errno 2] No such file or directory: '/dev/serial0'
[INFO] Retrying in 3 seconds...
```
*(Note: Error message will vary based on whether the port exists but has no data, or doesn't exist at all. If the port exists but ArduPilot isn't sending data, it will time out waiting for heartbeat).*

### To stop:
Press `Ctrl+C`. You will see:
```text
[INFO] Keyboard interrupt received.
[INFO] Closing connection...
AEROSAR MAVLink service stopped.
```
