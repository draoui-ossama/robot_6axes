import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/ossama/Desktop/ROBOTICS/first_exemple/ros2_ws/install/test_robot'
