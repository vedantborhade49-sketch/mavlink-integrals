import socket
import threading
import time
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from network.protocol import encode_message, MessageBuffer

class TCPServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket = None
        self.client_address = None
        self.running = False
        self.client_connected = False

    def start(self):
        self.running = True
        try:
            self.server_socket.bind((config.PI_HOST, config.PI_PORT))
            self.server_socket.listen(1)
            print("[INFO] Starting AEROSAR TCP server")
            print(f"[INFO] Listening on {config.PI_HOST}:{config.PI_PORT}")
            
            # Start heartbeat thread
            heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            heartbeat_thread.start()

            self._accept_loop()
        except Exception as e:
            print(f"[ERROR] Failed to start server: {e}")
            self.running = False

    def _accept_loop(self):
        while self.running:
            print("[INFO] Waiting for computing device...")
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                self.client_socket.settimeout(config.SOCKET_TIMEOUT)
                self.client_connected = True
                print(f"[INFO] Client connected: {self.client_address[0]}")
                self._receive_loop()
            except Exception as e:
                if self.running:
                    print(f"[ERROR] Accept error: {e}")
                    time.sleep(1)

    def _receive_loop(self):
        msg_buffer = MessageBuffer()
        
        while self.client_connected and self.running:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    print("[WARNING] Client disconnected")
                    break
                
                msg_buffer.add_data(data)
                for msg in msg_buffer.get_messages():
                    self._handle_message(msg)
                    
            except socket.timeout:
                # Normal timeout, just continue listening
                continue
            except ConnectionResetError:
                print("[WARNING] Client forcibly disconnected")
                break
            except Exception as e:
                print(f"[ERROR] Connection error: {e}")
                break
                
        self._cleanup_client()

    def _handle_message(self, msg):
        msg_type = msg.get("type", "unknown")
        
        if msg_type == "heartbeat":
            print(f"[INFO] Received heartbeat from client (ts: {msg.get('timestamp')})")
            # Send ACK
            ack_msg = {"type": "ack", "message_id": msg.get("timestamp")}
            self.send_message(ack_msg)
            print("[INFO] Sent ACK")
        elif msg_type == "ack":
            pass # We received an ack for our heartbeat
        else:
            print(f"[INFO] Received message: {msg}")

    def send_message(self, data_dict):
        if self.client_connected and self.client_socket:
            encoded_data = encode_message(data_dict)
            if encoded_data:
                try:
                    self.client_socket.sendall(encoded_data)
                    return True
                except Exception as e:
                    print(f"[ERROR] Failed to send message: {e}")
                    self._cleanup_client()
        return False

    def _heartbeat_loop(self):
        while self.running:
            if self.client_connected:
                hb_msg = {
                    "type": "heartbeat",
                    "timestamp": time.time(),
                    "source": "pi"
                }
                self.send_message(hb_msg)
            time.sleep(2) # Send heartbeat every 2 seconds

    def _cleanup_client(self):
        self.client_connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None

    def stop(self):
        self.running = False
        self._cleanup_client()
        try:
            self.server_socket.close()
        except:
            pass

if __name__ == "__main__":
    server = TCPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down server")
        server.stop()
