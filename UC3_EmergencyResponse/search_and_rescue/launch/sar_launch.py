import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():

    cloud = Node(
            package='search_and_rescue',
            executable='cloud',
            name='cloud'
        )
    
    edge = Node(
            package='search_and_rescue',
            executable='edge',
            name='edge'
        )
    
    fc = Node(
            package='search_and_rescue',
            executable='fc',
            name='fc'
        )
    
    nn = Node(
            package='search_and_rescue',
            executable='nn',
            name='nn'
    )
    
    # Create the launch description and populate
    ld = LaunchDescription()

    ld.add_action(cloud)
    ld.add_action(edge)
    ld.add_action(fc)
    ld.add_action(nn)

    return ld