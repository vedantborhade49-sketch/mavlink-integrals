# AEROSAR Vehicle State Message
# Represents the parsed telemetry from the flight controller

builtin_interfaces/Time timestamp

bool connected
bool armed
string flight_mode

# Position
float64 latitude           # degrees
float64 longitude          # degrees
float32 altitude           # meters (AMSL)
float32 relative_altitude  # meters (above home)

# Attitude
float32 roll               # radians
float32 pitch              # radians
float32 yaw                # radians

# Additional Telemetry
float32 ground_speed       # m/s
uint8 gps_fix              # 0-1: no fix, 2: 2D fix, 3: 3D fix
uint8 satellites           # number of visible satellites

# Battery
float32 battery_voltage    # volts
uint8 battery_remaining    # percentage (0-100)
