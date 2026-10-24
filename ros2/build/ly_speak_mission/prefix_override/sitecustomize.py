import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/smart/LY_speak_ws/ros2/install/ly_speak_mission'
