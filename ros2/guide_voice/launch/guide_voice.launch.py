import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # 讲解任务自己的 guide_voice 包，配置也放在自己包里（不再引用巡检的
    # system_manager 包）
    config = os.path.join(
        get_package_share_directory("guide_voice"), "config", "tts.default.yaml"
    )
    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="false"),
        Node(
            package="guide_voice",
            executable="tts_python_node",
            name="guide_tts_node",
            output="screen",
            respawn=True,
            respawn_delay=5.0,
            parameters=[config, {"use_sim_time": ParameterValue(LaunchConfiguration("use_sim_time"), value_type=bool)}],
        ),
    ])
