from setuptools import setup
import os
from glob import glob

package_name = 'aerosar_navigation'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Dev',
    maintainer_email='dev@example.com',
    description='Path Planning and Navigation Architecture for AEROSAR',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Placeholders for future ROS runtime execution
            'navigation_manager = aerosar_navigation.navigation_manager:main',
            'planner_interface = aerosar_navigation.planner_interface:main',
        ],
    },
)
