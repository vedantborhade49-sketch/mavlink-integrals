#!/usr/bin/env python3
import rclpy  # type: ignore
from rclpy.node import Node  # type: ignore

# Import our custom message
from aerosar_msgs.msg import VehicleState as ROSVehicleState  # type: ignore

class TestSubscriber(Node):
    def __init__(self):
        super().__init__('test_subscriber')
        
        self.subscription = self.create_subscription(
            ROSVehicleState,
            '/aerosar/vehicle/state',
            self.listener_callback,
            10
        )
        self.get_logger().info("Test Subscriber initialized. Listening for real vehicle telemetry...")

    def listener_callback(self, msg):
        self.get_logger().info(
            f"\n=== REAL VEHICLE STATE ==="
            f"\nMode: {msg.flight_mode} | Armed: {msg.armed}"
            f"\nPosition: [{msg.latitude:.6f}, {msg.longitude:.6f}, {msg.altitude:.2f}m]"
            f"\nAttitude: [R: {msg.roll:.2f}, P: {msg.pitch:.2f}, Y: {msg.yaw:.2f}]"
            f"\nBattery: {msg.battery_voltage:.2f}V ({msg.battery_remaining}%)"
            f"\n=========================="
        )

def main(args=None):
    rclpy.init(args=args)
    node = TestSubscriber()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received.")
    finally:
        rclpy.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
