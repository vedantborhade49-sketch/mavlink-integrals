import socket
import threading
import time
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from network.protocol import encode_message, MessageBuffer
from vehicle_state import VehicleState

class TCPClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.running = False
        
        # STEP 3: Local normalized vehicle state
        self.vehicle_state = VehicleState()

    def get_vehicle_state(self):
        """
        Returns the latest normalized vehicle state received from the Raspberry Pi.
        """
        return self.vehicle_state

    def start(self):
        self.running = True
        print("[INFO] Starting AEROSAR TCP client")
        
        # Start heartbeat thread
        heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        heartbeat_thread.start()

        self._connection_loop()

    def _connection_loop(self):
        while self.running:
            if not self.connected:
                print(f"[INFO] Connecting to Raspberry Pi at {config.PI_IP}:{config.PI_PORT}...")
                try:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.settimeout(config.CONNECT_TIMEOUT)
                    self.socket.connect((config.PI_IP, config.PI_PORT))
                    
                    self.socket.settimeout(config.SOCKET_TIMEOUT)
                    self.connected = True
                    print("[INFO] TCP connection established")
                    
                    self._receive_loop()
                except (ConnectionRefusedError, socket.timeout, OSError) as e:
                    print("[WARNING] Raspberry Pi unavailable")
                    print(f"[INFO] Retrying in {config.RECONNECT_DELAY} seconds...")
                    self._cleanup_socket()
                    time.sleep(config.RECONNECT_DELAY)
            else:
                time.sleep(1)

    def _receive_loop(self):
        msg_buffer = MessageBuffer()
        
        while self.connected and self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    print("[WARNING] Connection lost (server closed)")
                    break
                
                msg_buffer.add_data(data)
                for msg in msg_buffer.get_messages():
                    self._handle_message(msg)
                    
            except socket.timeout:
                continue
            except ConnectionResetError:
                print("[WARNING] Connection reset by server")
                break
            except Exception as e:
                print(f"[ERROR] Connection error: {e}")
                break
                
        self._cleanup_socket()

    def _handle_message(self, msg):
        msg_type = msg.get("type", "unknown")
        
        if msg_type == "telemetry":
            data = msg.get("data")
            if data:
                self.vehicle_state.update_from_dict(data)
                if not self.vehicle_state.connected:
                    print("[INFO] Vehicle telemetry: UNAVAILABLE")
                else:
                    print(f"[INFO] Vehicle telemetry: AVAILABLE | Mode: {self.vehicle_state.flight_mode} | Armed: {self.vehicle_state.armed}")
                
        elif msg_type == "status":
            print(f"[INFO] Server Status: {msg.get('data')}")
            
        elif msg_type == "heartbeat":
            # Send ACK silently without spamming log
            ack_msg = {"type": "ack", "message_id": msg.get("timestamp")}
            self.send_message(ack_msg)
            
        elif msg_type == "ack":
            pass
            
        else:
            print(f"[INFO] Received unknown message type: {msg_type}")

    def send_message(self, data_dict):
        if self.connected and self.socket:
            encoded_data = encode_message(data_dict)
            if encoded_data:
                try:
                    self.socket.sendall(encoded_data)
                    return True
                except Exception as e:
                    print(f"[ERROR] Failed to send message: {e}")
                    self._cleanup_socket()
        return False

    def _heartbeat_loop(self):
        while self.running:
            if self.connected:
                hb_msg = {
                    "type": "heartbeat",
                    "timestamp": time.time(),
                    "source": "client"
                }
                self.send_message(hb_msg)
            time.sleep(2)

    def _cleanup_socket(self):
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
            
        # Optional: Mark local vehicle state as disconnected if TCP dies
        # (Though we might want to keep the last known state)
        # self.vehicle_state.connected = False

    def stop(self):
        self.running = False
        self._cleanup_socket()

if __name__ == "__main__":
    client = TCPClient()
    try:
        client.start()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down client")
        client.stop()
