from setuptools import setup
import os
from glob import glob

package_name = 'aerosar_localization'

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
    description='Localization and state estimation for AEROSAR quadcopter',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'state_translator_node = aerosar_localization.state_translator_node:main',
            'static_tf_broadcaster = aerosar_localization.static_tf_broadcaster:main'
        ],
    },
)
