import os
from os.path import sep

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    urdf = [
        get_package_share_directory('urdf_sim_tutorial'),
        sep,
        LaunchConfiguration('model', default='urdf/r2d2.urdf')
    ]

    os.environ["GAZEBO_MODEL_PATH"] = os.environ["GAZEBO_MODEL_PATH"] \
                                      + ':' + get_package_share_directory("urdf_sim_tutorial") + "/meshes"

    debug = LaunchConfiguration('debug', default='false'),
    gui = LaunchConfiguration('gui', default='true'),
    paused = LaunchConfiguration('paused', default='false'),
    use_sim_time = LaunchConfiguration('use_sim_time', default='true'),
    headless = LaunchConfiguration('headless', default='false')

    return LaunchDescription([
        DeclareLaunchArgument(
            'paused',
            default_value='false'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true'
        ),
        DeclareLaunchArgument(
            'gui',
            default_value='true'
        ),
        DeclareLaunchArgument(
            'headless',
            default_value='false'
        ),
        DeclareLaunchArgument(
            'model',
            default_value='urdf/r2d2.urdf'
        ),

        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so',
                 '/usr/share/gazebo-9/worlds/willowgarage.world'],
            output='screen'
        ),
        Node(
            name='urdf_spawner',
            package='gazebo_ros',
            node_executable='spawn_entity.py',
            arguments=['-z', '1.0', '-unpause', '-entity', 'R2D2', '-file', urdf],
        ),
        Node(
            name='robot_state_publisher',
            package='robot_state_publisher',
            node_executable='robot_state_publisher',
            parameters=[{
                'publish_frequency': 30.0,
                'use_sim_time': use_sim_time
            }],
            arguments=[urdf]
        )
    ])
