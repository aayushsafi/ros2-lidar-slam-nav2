#!/bin/bash
source /opt/ros/jazzy/setup.bash
pkill -9 -f "gz sim"; pkill -9 -f ros_gz_bridge; pkill -9 -f static_transform_publisher; sleep 1
trap 'kill 0' EXIT
gz sim -s -r ~/lidar_learning/slam_world.sdf &
sleep 5
ros2 run ros_gz_bridge parameter_bridge \
  /scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan \
  /cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist \
  /odom@nav_msgs/msg/Odometry[gz.msgs.Odometry \
  /tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V \
  /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock &
ros2 run tf2_ros static_transform_publisher --z 0.22 --frame-id base_footprint --child-frame-id lidar_link &
ros2 run tf2_ros static_transform_publisher --frame-id base_footprint --child-frame-id base_link &
wait
