from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    TimerAction,
    LogInfo,
    RegisterEventHandler,
)
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart


def generate_launch_description():

    turtlesim = Node(
        package="turtlesim", executable="turtlesim_node", name="turtlesim"
    )

    kill_turtle = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/kill",
            "turtlesim/srv/Kill",
            "{name: turtle1}",
        ],
        output="screen",
    )

    spawn_turtle1 = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/spawn",
            "turtlesim/srv/Spawn",
            "{x: 2, y: 2, theta: 0.2, name: 'cherepaxa06_0'}",
        ],
        output="screen",
    )
    spawn_turtle2 = ExecuteProcess(
        cmd=[
            "ros2",
            "service",
            "call",
            "/spawn",
            "turtlesim/srv/Spawn",
            "{x: 6, y: 5, theta: 0.2, name: 'cherepaxa06_6'}",
        ],
        output="screen",
    )

    digit0 = Node(
        package="cherepaxa06",
        executable="cherepaxa06",
        name="cherepaxa06_0",
        parameters=[{"digit":0}],
        output="screen",
    )
    digit6 = Node(
        package="cherepaxa06",
        executable="cherepaxa06",
        name="cherepaxa06_6",
        parameters=[{"digit":6}],
        output="screen",
    )

    return LaunchDescription(
        [
            turtlesim,
            RegisterEventHandler(
                OnProcessStart(
                    target_action=turtlesim,
                    on_start=[
                        LogInfo(msg="Turtlesim started, spawning turtle"),
                        kill_turtle,
                        spawn_turtle1,
                        spawn_turtle2
                    ],
                )
            ),
            TimerAction(period=0.2, actions=[digit0, digit6]),
        ]
    )
