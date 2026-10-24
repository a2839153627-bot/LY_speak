# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target insp_interfaces::insp_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${insp_interfaces_TARGETS}.
if(insp_interfaces_TARGETS AND NOT TARGET insp_interfaces::insp_interfaces)
  add_library(insp_interfaces::insp_interfaces INTERFACE IMPORTED)
  set_target_properties(insp_interfaces::insp_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${insp_interfaces_TARGETS}")
endif()
