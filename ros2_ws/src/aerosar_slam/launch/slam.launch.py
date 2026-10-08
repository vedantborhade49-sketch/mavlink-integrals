import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='aerosar_slam',
            executable='visual_slam_node',
            name='visual_slam_node',
            output='screen'
        )
    ])
