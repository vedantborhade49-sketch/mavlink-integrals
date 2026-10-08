from setuptools import setup
import os
from glob import glob

package_name = 'aerosar_slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Dev',
    maintainer_email='dev@example.com',
    description='Visual SLAM and Mapping for AEROSAR quadcopter',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'visual_slam_node = aerosar_slam.visual_slam_node:main'
        ],
    },
)
