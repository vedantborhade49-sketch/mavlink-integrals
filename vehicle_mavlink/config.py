# config.py
# Configuration for the Raspberry Pi 5 to ArduPilot MAVLink connection

# The serial port used for MAVLink communication.
# IMPORTANT: Change this to match your actual Raspberry Pi UART configuration!
# Common values:
# - '/dev/serial0' (default Pi UART, usually mapped to ttyAMA0 or ttyS0)
# - '/dev/ttyAMA0'
# - 'COM3' (if testing on Windows)
SERIAL_PORT = "/dev/serial0"

# The baud rate for the connection. 
# 57600 is standard for ArduPilot telemetry ports.
BAUD_RATE = 57600

# How long to wait for a heartbeat (in seconds) before considering the connection failed/lost.
HEARTBEAT_TIMEOUT = 10

# Delay (in seconds) before attempting to reconnect after a failure.
RECONNECT_DELAY = 3

# TEST MODE
# When set to True, the script will not connect to a physical serial port.
# Instead, it will generate fake MAVLink messages to test the telemetry parsing.
# Physical hardware mode remains: TEST_MODE = False
TEST_MODE = True
