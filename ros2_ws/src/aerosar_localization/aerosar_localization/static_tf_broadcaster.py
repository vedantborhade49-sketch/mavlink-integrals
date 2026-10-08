#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math

def euler_to_quaternion(roll, pitch, yaw):
    qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
    qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
    qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
    return [qx, qy, qz, qw]

class StaticTfBroadcaster(Node):
    def __init__(self):
        super().__init__('static_tf_broadcaster')
        self.tf_static_broadcaster = StaticTransformBroadcaster(self)

        # Publish static transforms: base_link -> camera_link, base_link -> imu_link, base_link -> gps_link
        self.make_transforms()

    def make_transforms(self):
        now = self.get_clock().now().to_msg()
        transforms = []

        # 1. base_link -> camera_link (Front facing camera example)
        t_cam = TransformStamped()
        t_cam.header.stamp = now
        t_cam.header.frame_id = 'base_link'
        t_cam.child_frame_id = 'camera_link'
        t_cam.transform.translation.x = 0.1 # 10cm forward
        t_cam.transform.translation.y = 0.0
        t_cam.transform.translation.z = 0.05 # 5cm up
        
        # Standard ROS camera frame: z forward, x right, y down. 
        # But for base camera link, let's just point it forward
        q_cam = euler_to_quaternion(0, 0, 0)
        t_cam.transform.rotation.x = q_cam[0]
        t_cam.transform.rotation.y = q_cam[1]
        t_cam.transform.rotation.z = q_cam[2]
        t_cam.transform.rotation.w = q_cam[3]
        transforms.append(t_cam)

        # 2. base_link -> imu_link (Flight Controller)
        t_imu = TransformStamped()
        t_imu.header.stamp = now
        t_imu.header.frame_id = 'base_link'
        t_imu.child_frame_id = 'imu_link'
        t_imu.transform.translation.x = 0.0
        t_imu.transform.translation.y = 0.0
        t_imu.transform.translation.z = 0.0
        t_imu.transform.rotation.x = 0.0
        t_imu.transform.rotation.y = 0.0
        t_imu.transform.rotation.z = 0.0
        t_imu.transform.rotation.w = 1.0
        transforms.append(t_imu)
        
        # 3. base_link -> gps_link
        t_gps = TransformStamped()
        t_gps.header.stamp = now
        t_gps.header.frame_id = 'base_link'
        t_gps.child_frame_id = 'gps_link'
        t_gps.transform.translation.x = 0.0
        t_gps.transform.translation.y = 0.0
        t_gps.transform.translation.z = 0.1 # 10cm above
        t_gps.transform.rotation.x = 0.0
        t_gps.transform.rotation.y = 0.0
        t_gps.transform.rotation.z = 0.0
        t_gps.transform.rotation.w = 1.0
        transforms.append(t_gps)

        self.tf_static_broadcaster.sendTransform(transforms)

def main(args=None):
    rclpy.init(args=args)
    node = StaticTfBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
