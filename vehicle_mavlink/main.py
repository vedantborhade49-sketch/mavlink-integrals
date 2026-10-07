import time
import sys
import threading
import config
from connection import MAVLinkConnection
from telemetry import parse_telemetry, format_telemetry
from vehicle_state import VehicleState
from network.tcp_server import TCPServer

def telemetry_publisher_loop(server, v_state):
    """
    Periodically sends the normalized VehicleState over TCP to the computing device.
    """
    print("[INFO] Telemetry publisher started")
    while server.running:
        # Check if telemetry is stale
        stale = v_state.check_stale()
        
        # Send telemetry message
        telemetry_msg = {
            "type": "telemetry",
            "timestamp": time.time(),
            "data": v_state.to_dict()
        }
        server.send_message(telemetry_msg)
        
        # Optionally send status message too
        status_msg = {
            "type": "status",
            "data": {
                "mavlink_connected": not stale,
                "tcp_connected": server.client_connected,
                "telemetry_fresh": not stale
            }
        }
        server.send_message(status_msg)
        
        time.sleep(config.TELEMETRY_SEND_INTERVAL)

def main():
    print("=======================================")
    print(" AEROSAR MAVLink Telemetry Service")
    print("=======================================")
    
    # 1. Initialize Vehicle State
    v_state = VehicleState()
    
    # 2. Start TCP Server (Background Thread)
    tcp_server = TCPServer()
    server_thread = threading.Thread(target=tcp_server.start, daemon=True)
    server_thread.start()
    
    # Wait for server to fully bind
    time.sleep(0.5) 
    
    # 3. Start Telemetry Publisher (Background Thread)
    pub_thread = threading.Thread(target=telemetry_publisher_loop, args=(tcp_server, v_state), daemon=True)
    pub_thread.start()

    conn = MAVLinkConnection()
    
    try:
        while True:
            # 1. Attempt connection
            if not conn.connect():
                print(f"[WARNING] Waiting for real MAVLink heartbeat. Retrying in {config.RECONNECT_DELAY} seconds...")
                time.sleep(config.RECONNECT_DELAY)
                continue
                
            # 2. Wait for heartbeat
            if not conn.wait_for_heartbeat():
                conn.close()
                print(f"[WARNING] Waiting for real MAVLink heartbeat. Retrying in {config.RECONNECT_DELAY} seconds...")
                time.sleep(config.RECONNECT_DELAY)
                continue
                
            print("[INFO] MAVLink connected")
            print("[INFO] Starting MAVLink receive loop. Press Ctrl+C to stop.")
            
            # Throttle console output so we don't spam the terminal
            print_throttles = {
                "HEARTBEAT": 1.0,           
                "GLOBAL_POSITION_INT": 0.5, 
                "ATTITUDE": 0.5,            
                "SYS_STATUS": 1.0           
            }
            last_print_times = {k: 0 for k in print_throttles.keys()}
            
            while True:
                msg = conn.receive_message()
                
                if msg:
                    msg_type = msg.get_type()
                    
                    if msg_type in print_throttles:
                        parsed = parse_telemetry(msg)
                        if parsed:
                            # STEP 3: Update normalized vehicle state
                            v_state.update_from_parsed(parsed)
                            
                            # Print to console (throttled)
                            current_time = time.time()
                            if current_time - last_print_times[msg_type] >= print_throttles[msg_type]:
                                formatted = format_telemetry(parsed)
                                if formatted:
                                    print(formatted)
                                    last_print_times[msg_type] = current_time
                                    
                # Prevent 100% CPU usage in tight loop if no messages are arriving
                time.sleep(0.01)
                
    except KeyboardInterrupt:
        print("\n[INFO] Keyboard interrupt received.")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error in main loop: {e}")
    finally:
        print("[INFO] Closing MAVLink connection...")
        conn.close()
        print("[INFO] Shutting down TCP server...")
        tcp_server.stop()
        print("AEROSAR service stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
