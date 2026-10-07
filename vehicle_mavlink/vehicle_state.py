import time
import config

class VehicleState:
    """
    Maintains the normalized state of the vehicle.
    """
    def __init__(self):
        self.connected = False
        self.armed = False
        self.flight_mode = "UNKNOWN"
        
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.relative_altitude = 0.0
        
        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        
        self.ground_speed = 0.0
        self.gps_fix = 0
        self.satellites = 0
        
        self.battery_voltage = 0.0
        self.battery_remaining = 0
        
        self.last_update_time = 0.0

    def update_from_parsed(self, parsed_data):
        """
        Updates the internal state from the parsed telemetry dictionary.
        """
        if not parsed_data:
            return
            
        msg_type = parsed_data.get("type")
        self.last_update_time = time.time()
        self.connected = True
        
        if msg_type == "HEARTBEAT":
            self.armed = parsed_data.get("armed", False)
            mode = parsed_data.get("mode")
            # Convert numeric custom_mode to string if possible, or just stringify
            if mode is not None:
                self.flight_mode = str(mode)
                
        elif msg_type == "GLOBAL_POSITION_INT":
            self.latitude = parsed_data.get("lat", 0.0)
            self.longitude = parsed_data.get("lon", 0.0)
            self.altitude = parsed_data.get("alt", 0.0)
            self.relative_altitude = parsed_data.get("relative_alt", 0.0)
            
        elif msg_type == "ATTITUDE":
            self.roll = parsed_data.get("roll", 0.0)
            self.pitch = parsed_data.get("pitch", 0.0)
            self.yaw = parsed_data.get("yaw", 0.0)
            
        elif msg_type == "SYS_STATUS":
            self.battery_voltage = parsed_data.get("voltage_battery", 0.0)
            self.battery_remaining = parsed_data.get("battery_remaining", 0)

    def check_stale(self):
        """
        Checks if the telemetry data is stale. If so, marks connected=False.
        """
        if self.connected and (time.time() - self.last_update_time > config.TELEMETRY_STALE_TIMEOUT):
            self.connected = False
            return True
        return False

    def update_from_dict(self, data_dict):
        """
        Updates the internal state directly from a dictionary (e.g. received over TCP).
        """
        if not data_dict:
            return
            
        self.connected = data_dict.get("connected", False)
        self.armed = data_dict.get("armed", False)
        self.flight_mode = data_dict.get("flight_mode", "UNKNOWN")
        
        self.latitude = data_dict.get("latitude", 0.0)
        self.longitude = data_dict.get("longitude", 0.0)
        self.altitude = data_dict.get("altitude", 0.0)
        self.relative_altitude = data_dict.get("relative_altitude", 0.0)
        
        self.roll = data_dict.get("roll", 0.0)
        self.pitch = data_dict.get("pitch", 0.0)
        self.yaw = data_dict.get("yaw", 0.0)
        
        self.ground_speed = data_dict.get("ground_speed", 0.0)
        self.gps_fix = data_dict.get("gps_fix", 0)
        self.satellites = data_dict.get("satellites", 0)
        
        self.battery_voltage = data_dict.get("battery_voltage", 0.0)
        self.battery_remaining = data_dict.get("battery_remaining", 0)
        
        self.last_update_time = data_dict.get("timestamp", time.time())

    def to_dict(self):
        """
        Returns the normalized vehicle state as a dictionary for TCP transmission.
        """
        self.check_stale() # Update connected status before dumping
        
        return {
            "connected": self.connected,
            "armed": self.armed,
            "flight_mode": self.flight_mode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "relative_altitude": self.relative_altitude,
            "roll": self.roll,
            "pitch": self.pitch,
            "yaw": self.yaw,
            "ground_speed": self.ground_speed,
            "gps_fix": self.gps_fix,
            "satellites": self.satellites,
            "battery_voltage": self.battery_voltage,
            "battery_remaining": self.battery_remaining,
            "timestamp": self.last_update_time
        }
