# AEROSAR Hardware-Dependent Parameters

The following parameters remain strictly undefined (marked as `PENDING HARDWARE VALIDATION`) because generating fake assumptions violates the core safety rules. They must be physically validated and updated before flight.

## Flight Controller & Communication
- SpeedyBee FC exact model
- FC ↔ Pi UART port (Currently assumed `/dev/serial0` for standard Pi setup, requires verification)
- UART baud rate (Currently `57600`, requires FC matching)
- ArduPilot parameters (e.g., `SR0_EXTRA1` stream rates)
- MAVLink configuration (SysID, CompID overrides if any)

## Sensors & Payload
- Pi camera exact model and interface (CSI vs USB)
- GNSS exact model and update rate
- IMU exact model (onboard FC or external)
- LiDAR (Model, interface, minimum/maximum range)
- Sensor mounting offsets (X, Y, Z translations for TF tree)
- Sensor frame transforms (Rotations for TF tree)

## Flight Dynamics (Vehicle Constraints)
- Vehicle physical dimensions (for collision boundary)
- Maximum horizontal speed
- Maximum vertical speed (climb rate)
- Maximum descent rate
- Minimum safe altitude
- Maximum permitted altitude
- Minimum turn radius
- Maximum acceleration
- Battery characteristics (Voltage sag profiles, capacity, cells)
- Flight envelope (wind resistance, payload limits)
