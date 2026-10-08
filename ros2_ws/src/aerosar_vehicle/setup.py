from setuptools import find_packages, setup

package_name = 'aerosar_vehicle'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AEROSAR Team',
    maintainer_email='dev@aerosar.local',
    description='AEROSAR Python TCP-to-ROS 2 Interface',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vehicle_state_node = aerosar_vehicle.vehicle_state_node:main',
            'test_subscriber = aerosar_vehicle.test_subscriber:main'
        ],
    },
)
