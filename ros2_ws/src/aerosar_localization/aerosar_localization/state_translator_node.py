#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from aerosar_msgs.msg import VehicleState as ROSVehicleState
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, NavSatFix
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster

def euler_to_quaternion(roll, pitch, yaw):
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class StateTranslatorNode(Node):
    def __init__(self):
        super().__init__('state_translator_node')
        
        self.subscription = self.create_subscription(
            ROSVehicleState,
            '/aerosar/vehicle/state',
            self.state_callback,
            10
        )
        
        self.odom_pub = self.create_publisher(Odometry, '/aerosar/localization/odom', 10)
        self.imu_pub = self.create_publisher(Imu, '/aerosar/sensors/imu', 10)
        self.gps_pub = self.create_publisher(NavSatFix, '/aerosar/sensors/gps', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info("StateTranslatorNode initialized. Waiting for vehicle state...")

    def state_callback(self, msg: ROSVehicleState):
        if not msg.connected:
            return

        now = self.get_clock().now().to_msg()
        
        # We assume the Flight Controller sends real data. Do not fake it.
        # 1. Publish NavSatFix
        gps_msg = NavSatFix()
        gps_msg.header.stamp = now
        gps_msg.header.frame_id = "gps_link"
        gps_msg.latitude = msg.latitude
        gps_msg.longitude = msg.longitude
        gps_msg.altitude = msg.altitude
        # Add basic covariance based on GPS fix type
        gps_msg.status.status = msg.gps_fix - 1 if msg.gps_fix > 0 else -1
        self.gps_pub.publish(gps_msg)
        
        # 2. Publish IMU
        imu_msg = Imu()
        imu_msg.header.stamp = now
        imu_msg.header.frame_id = "imu_link"
        q = euler_to_quaternion(msg.roll, msg.pitch, msg.yaw)
        imu_msg.orientation.x = q[0]
        imu_msg.orientation.y = q[1]
        imu_msg.orientation.z = q[2]
        imu_msg.orientation.w = q[3]
        self.imu_pub.publish(imu_msg)
        
        # 3. Publish Odometry and TF (odom -> base_link)
        # Assuming the state is fused by ArduPilot EKF.
        odom_msg = Odometry()
        odom_msg.header.stamp = now
        odom_msg.header.frame_id = "odom"
        odom_msg.child_frame_id = "base_link"
        
        # For a full system, you would convert Lat/Lon to local Cartesian coordinates (e.g. UTM or local tangent plane).
        # We'll use a naive or external translation if available, but for now we set relative_altitude and let
        # the localization package or external node handle global to local. 
        # We will populate orientation for Odometry.
        odom_msg.pose.pose.orientation = imu_msg.orientation
        
        # Assuming velocity is provided in future updates, currently we just have ground_speed
        odom_msg.twist.twist.linear.x = msg.ground_speed
        self.odom_pub.publish(odom_msg)

        # TF Broadcast: odom -> base_link
        # For simplicity, we just broadcast orientation here. Position should be handled by a real EKF 
        # (like robot_localization) fusing GPS + IMU + Vision.
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = msg.relative_altitude
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = StateTranslatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
