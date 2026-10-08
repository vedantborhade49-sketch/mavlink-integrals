#!/usr/bin/env python3
import sys
import os
import rclpy  # type: ignore
from rclpy.node import Node  # type: ignore
from std_msgs.msg import String  # type: ignore

# IMPORTANT: Inject the absolute path to the vehicle_mavlink directory so we can reuse Step 3
# This allows ROS to directly consume the exact same TCPClient and VehicleState logic
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Robustly find WORKSPACE_ROOT by traversing up until we leave ros2_ws
current_dir = SCRIPT_DIR
while current_dir and 'ros2_ws' in current_dir:
    current_dir = os.path.dirname(current_dir)
    
WORKSPACE_ROOT = current_dir
VEHICLE_MAVLINK_DIR = os.path.join(WORKSPACE_ROOT, 'vehicle_mavlink')
if VEHICLE_MAVLINK_DIR not in sys.path:
    sys.path.append(VEHICLE_MAVLINK_DIR)

try:
    from network.tcp_client import TCPClient  # type: ignore
except ImportError as e:
    print(f"FATAL: Could not import TCPClient. Ensure vehicle_mavlink is accessible. {e}")
    sys.exit(1)

# Import our custom message
from aerosar_msgs.msg import VehicleState as ROSVehicleState  # type: ignore

class VehicleStateNode(Node):
    def __init__(self):
        super().__init__('vehicle_state_node')
        
        # Publishers
        self.state_pub = self.create_publisher(ROSVehicleState, '/aerosar/vehicle/state', 10)
        self.status_pub = self.create_publisher(String, '/aerosar/vehicle/status', 10)
        
        # Initialize TCP Client from Step 3
        self.tcp_client = TCPClient()
        self.get_logger().info("Starting TCP Client background thread...")
        
        import threading
        self.client_thread = threading.Thread(target=self.tcp_client.start, daemon=True)
        self.client_thread.start()
        
        # Publish at 10Hz
        self.timer = self.create_timer(0.1, self.publish_state)
        self.get_logger().info("VehicleStateNode initialized. Waiting for real telemetry...")

    def publish_state(self):
        # 1. Publish Status
        status_msg = String()
        v_state = self.tcp_client.get_vehicle_state()
        
        if not self.tcp_client.connected:
            status_msg.data = "TCP: DISCONNECTED | Telemetry: UNAVAILABLE"
            self.status_pub.publish(status_msg)
            # DO NOT PUBLISH FAKE TELEMETRY
            return
            
        if not v_state.connected:
            status_msg.data = "MAVLink: DISCONNECTED | TCP: CONNECTED | Telemetry: UNAVAILABLE"
            self.status_pub.publish(status_msg)
            # DO NOT PUBLISH FAKE TELEMETRY
            return
            
        status_msg.data = "MAVLink: CONNECTED | TCP: CONNECTED | Telemetry: AVAILABLE"
        self.status_pub.publish(status_msg)
        
        # 2. Publish Real Telemetry
        state_msg = ROSVehicleState()
        state_msg.timestamp = self.get_clock().now().to_msg()
        
        state_msg.connected = v_state.connected
        state_msg.armed = v_state.armed
        state_msg.flight_mode = str(v_state.flight_mode)
        
        state_msg.latitude = float(v_state.latitude)
        state_msg.longitude = float(v_state.longitude)
        state_msg.altitude = float(v_state.altitude)
        state_msg.relative_altitude = float(v_state.relative_altitude)
        
        state_msg.roll = float(v_state.roll)
        state_msg.pitch = float(v_state.pitch)
        state_msg.yaw = float(v_state.yaw)
        
        state_msg.ground_speed = float(v_state.ground_speed)
        state_msg.gps_fix = int(v_state.gps_fix)
        state_msg.satellites = int(v_state.satellites)
        
        state_msg.battery_voltage = float(v_state.battery_voltage)
        state_msg.battery_remaining = int(v_state.battery_remaining)
        
        self.state_pub.publish(state_msg)

    def stop(self):
        self.get_logger().info("Shutting down cleanly...")
        self.tcp_client.stop()
        if self.client_thread.is_alive():
            self.client_thread.join(timeout=2.0)

def main(args=None):
    rclpy.init(args=args)
    node = VehicleStateNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received.")
    finally:
        node.stop()
        rclpy.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
