cmake_minimum_required(VERSION 3.8)
project(insp_interfaces)
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/RecognizeInspection.srv"
  "srv/Speak.srv"
)
ament_package()
