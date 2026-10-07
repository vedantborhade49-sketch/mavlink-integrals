# connection.py
import time
from pymavlink import mavutil
import config

class MockMAVLinkConnection:
    """A mock connection for testing without physical hardware."""
    def __init__(self):
        self.start_time = time.time()
        self.last_msg_time = 0
        self.msg_index = 0
        self.target_system = 1
        self.target_component = 1
        
    class MockMessage:
        def __init__(self, type_name, **kwargs):
            self._type = type_name
            for k, v in kwargs.items():
                setattr(self, k, v)
        def get_type(self):
            return self._type

    def recv_match(self, type=None, blocking=False, timeout=0):
        # Handle heartbeat wait differently from telemetry loop
        if type == 'HEARTBEAT' and blocking:
            time.sleep(1) # Simulate connection delay
            return self.MockMessage("HEARTBEAT", type=2, autopilot=3, base_mode=81, custom_mode=0, system_status=4)
            
        current_time = time.time()
        if current_time - self.last_msg_time < 0.2: # Rate limit mock messages (5Hz)
            return None
        self.last_msg_time = current_time
        
        msgs = [
            self.MockMessage("HEARTBEAT", type=2, autopilot=3, base_mode=81, custom_mode=0, system_status=4),
            self.MockMessage("GLOBAL_POSITION_INT", lat=377749000, lon=-1224194000, alt=10000, relative_alt=5000),
            self.MockMessage("ATTITUDE", roll=0.1, pitch=-0.05, yaw=1.5),
            self.MockMessage("SYS_STATUS", voltage_battery=12400, current_battery=1500, battery_remaining=95)
        ]
        
        msg = msgs[self.msg_index]
        self.msg_index = (self.msg_index + 1) % len(msgs)
        return msg
        
    def close(self):
        pass

class MAVLinkConnection:
    def __init__(self):
        self.master = None

    def connect(self):
        """
        Attempts to open the serial connection.
        """
        if config.TEST_MODE:
            print("[INFO] TEST_MODE is True. Using Mock MAVLink connection.")
            self.master = MockMAVLinkConnection()
            return True

        print(f"[INFO] Attempting to open serial connection on {config.SERIAL_PORT} at {config.BAUD_RATE} baud...")
        try:
            # Use mavutil.mavlink_connection to establish the connection
            self.master = mavutil.mavlink_connection(
                config.SERIAL_PORT, 
                baud=config.BAUD_RATE
            )
            print("[INFO] Serial connection opened successfully.")
            return True
        except Exception as e:
            print(f"[ERROR] Serial connection failed: {e}")
            return False

    def wait_for_heartbeat(self):
        """
        Waits for the first heartbeat message from ArduPilot.
        """
        if not self.master:
            print("[ERROR] Cannot wait for heartbeat: Connection not initialized.")
            return False

        print("[INFO] Waiting for ArduPilot heartbeat...")
        try:
            # Wait for a heartbeat with the configured timeout
            heartbeat = self.master.recv_match(type='HEARTBEAT', blocking=True, timeout=config.HEARTBEAT_TIMEOUT)
            
            if heartbeat:
                sys_id = self.master.target_system
                comp_id = self.master.target_component
                
                print("[INFO] Heartbeat received.")
                print(f"[INFO] System ID: {sys_id}")
                print(f"[INFO] Component ID: {comp_id}")
                print("[INFO] MAVLink connection established.")
                return True
            else:
                print(f"[ERROR] No heartbeat received within {config.HEARTBEAT_TIMEOUT} seconds.")
                return False
        except Exception as e:
            print(f"[ERROR] Exception while waiting for heartbeat: {e}")
            return False

    def receive_message(self):
        """
        Receives a single MAVLink message if available. Non-blocking.
        """
        if not self.master:
            return None
            
        try:
            msg = self.master.recv_match(blocking=False)
            return msg
        except Exception as e:
            # Catching serial read errors (e.g. device disconnected)
            print(f"[ERROR] Error receiving message: {e}")
            return None

    def close(self):
        """
        Closes the connection cleanly.
        """
        if self.master:
            try:
                self.master.close()
                self.master = None
            except Exception as e:
                print(f"[ERROR] Error closing connection: {e}")
