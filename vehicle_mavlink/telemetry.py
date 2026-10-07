# telemetry.py

def parse_telemetry(msg):
    """
    Parses a single MAVLink message and returns a dictionary of extracted values,
    or None if the message type is not supported in this simple telemetry parser.
    """
    if msg is None:
        return None

    msg_type = msg.get_type()
    data = {"type": msg_type}

    if msg_type == "HEARTBEAT":
        # Extract basic heartbeat information
        data["mode"] = msg.custom_mode  # Custom mode specific to ArduPilot
        data["armed"] = (msg.base_mode & 128) != 0 # MAV_MODE_FLAG_SAFETY_ARMED
        data["system_status"] = msg.system_status
        return data

    elif msg_type == "GLOBAL_POSITION_INT":
        data["lat"] = msg.lat / 1e7
        data["lon"] = msg.lon / 1e7
        data["alt"] = msg.alt / 1000.0  # mm to meters
        data["relative_alt"] = msg.relative_alt / 1000.0
        return data

    elif msg_type == "ATTITUDE":
        data["roll"] = msg.roll
        data["pitch"] = msg.pitch
        data["yaw"] = msg.yaw
        return data

    elif msg_type == "SYS_STATUS":
        data["voltage_battery"] = msg.voltage_battery / 1000.0  # mV to V
        data["current_battery"] = msg.current_battery / 100.0  # cA to A
        data["battery_remaining"] = msg.battery_remaining
        return data

    return None

def format_telemetry(parsed_data):
    """
    Formats the parsed telemetry data into a readable string.
    """
    if not parsed_data:
        return ""
    
    msg_type = parsed_data.get("type")
    
    if msg_type == "HEARTBEAT":
        return f"HEARTBEAT | Mode: {parsed_data.get('mode')}, Armed: {parsed_data.get('armed')}"
    
    elif msg_type == "GLOBAL_POSITION_INT":
        return f"POSITION  | Lat: {parsed_data.get('lat'):.6f}, Lon: {parsed_data.get('lon'):.6f}, Alt: {parsed_data.get('alt'):.2f}m"
        
    elif msg_type == "ATTITUDE":
        return f"ATTITUDE  | Roll: {parsed_data.get('roll'):.2f}, Pitch: {parsed_data.get('pitch'):.2f}, Yaw: {parsed_data.get('yaw'):.2f}"
        
    elif msg_type == "SYS_STATUS":
        return f"SYSTEM    | Battery: {parsed_data.get('voltage_battery'):.2f}V, {parsed_data.get('battery_remaining')}%"
    
    return ""
