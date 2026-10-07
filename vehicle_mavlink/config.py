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

# ==========================================
# STEP 2: TCP NETWORK CONFIGURATION
# ==========================================

# Server settings (Raspberry Pi)
PI_HOST = "0.0.0.0"      # Bind to all interfaces
PI_PORT = 5000           # TCP Port

# Client settings (Computing Device)
# Change this to the actual Raspberry Pi IP address when testing over Wi-Fi/Ethernet
# For local testing on the same machine, use "127.0.0.1"
PI_IP = "127.0.0.1"      

# Connection settings
CONNECT_TIMEOUT = 5      # Seconds to wait for connection
RECONNECT_DELAY = 3      # Seconds before retrying connection
SOCKET_TIMEOUT = 5       # General socket timeout

# Telemetry Settings
TELEMETRY_SEND_INTERVAL = 0.2    # 5 updates per second
TELEMETRY_STALE_TIMEOUT = 2.0    # 2 seconds without updates is stale
