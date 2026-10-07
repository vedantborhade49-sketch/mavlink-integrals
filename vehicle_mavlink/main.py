# main.py
import time
import sys
import config
from connection import MAVLinkConnection
from telemetry import parse_telemetry, format_telemetry

def main():
    print("=======================================")
    print(" AEROSAR MAVLink Telemetry Service")
    print("=======================================")
    
    conn = MAVLinkConnection()
    
    try:
        while True:
            # 1. Attempt connection
            if not conn.connect():
                print(f"[INFO] Retrying in {config.RECONNECT_DELAY} seconds...")
                time.sleep(config.RECONNECT_DELAY)
                continue
                
            # 2. Wait for heartbeat
            if not conn.wait_for_heartbeat():
                conn.close()
                print(f"[INFO] Retrying in {config.RECONNECT_DELAY} seconds...")
                time.sleep(config.RECONNECT_DELAY)
                continue
                
            # 3. Telemetry Loop
            print("[INFO] Starting telemetry loop. Press Ctrl+C to stop.")
            
            # Throttle output: print each supported message type only so often (in seconds)
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
                        current_time = time.time()
                        if current_time - last_print_times[msg_type] >= print_throttles[msg_type]:
                            parsed = parse_telemetry(msg)
                            if parsed:
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
        print("[INFO] Closing connection...")
        conn.close()
        print("AEROSAR MAVLink service stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
