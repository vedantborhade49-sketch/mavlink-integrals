# connection.py
import time
from pymavlink import mavutil
import config


class MAVLinkConnection:
    def __init__(self):
        self.master = None

    def connect(self):
        """
        Attempts to open the serial connection.
        """
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
