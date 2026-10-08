import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='aerosar_localization',
            executable='state_translator_node',
            name='state_translator_node',
            output='screen'
        ),
        Node(
            package='aerosar_localization',
            executable='static_tf_broadcaster',
            name='static_tf_broadcaster',
            output='screen'
        )
    ])
