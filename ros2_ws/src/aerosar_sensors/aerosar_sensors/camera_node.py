#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher_ = self.create_publisher(Image, '/aerosar/sensors/camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.bridge = CvBridge()

        # The camera index (0 is usually the default USB/built-in camera)
        self.camera_index = 0
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            self.get_logger().error(f"Camera unavailable at index {self.camera_index}.")
        else:
            self.get_logger().info(f"Camera successfully connected at index {self.camera_index}.")

    def timer_callback(self):
        if not self.cap.isOpened():
            # If camera is unavailable, report it and do not send fake data.
            self.get_logger().warn("Camera unavailable. Waiting for hardware...", throttle_duration_sec=5.0)
            # Try to reconnect
            self.cap = cv2.VideoCapture(self.camera_index)
            return

        ret, frame = self.cap.read()
        if not ret:
            self.get_logger().error("Camera frame read failed. Device may have disconnected.")
            self.cap.release()
            return

        # We have a real frame, publish it
        msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "camera_link"
        self.publisher_.publish(msg)

    def destroy_node(self):
        if self.cap.isOpened():
            self.cap.release()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
