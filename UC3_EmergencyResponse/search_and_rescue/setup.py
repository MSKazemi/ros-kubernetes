import os
from glob import glob
from setuptools import setup

package_name = 'search_and_rescue'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='smengozzi',
    maintainer_email='sebastiano.mengozzi@studio.unibo.it',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cloud = search_and_rescue.cloud_node:main',
            'edge = search_and_rescue.edge_node:main',
            'fc = search_and_rescue.fc_node:main',
            'nn = search_and_rescue.nnctrl_node:main'
        ],
    },
)
