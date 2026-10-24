// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__STRUCT_H_
#define INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'algorithm'
// Member 'image_path'
// Member 'output_dir'
// Member 'resource_dir'
// Member 'task_dir'
// Member 'point_name'
// Member 'node_type'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/RecognizeInspection in the package insp_interfaces.
typedef struct insp_interfaces__srv__RecognizeInspection_Request
{
  rosidl_runtime_c__String algorithm;
  rosidl_runtime_c__String image_path;
  rosidl_runtime_c__String output_dir;
  rosidl_runtime_c__String resource_dir;
  rosidl_runtime_c__String task_dir;
  int32_t point_id;
  rosidl_runtime_c__String point_name;
  rosidl_runtime_c__String node_type;
} insp_interfaces__srv__RecognizeInspection_Request;

// Struct for a sequence of insp_interfaces__srv__RecognizeInspection_Request.
typedef struct insp_interfaces__srv__RecognizeInspection_Request__Sequence
{
  insp_interfaces__srv__RecognizeInspection_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} insp_interfaces__srv__RecognizeInspection_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'result_json'
// Member 'visualization_path'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/RecognizeInspection in the package insp_interfaces.
typedef struct insp_interfaces__srv__RecognizeInspection_Response
{
  bool success;
  rosidl_runtime_c__String message;
  rosidl_runtime_c__String result_json;
  rosidl_runtime_c__String visualization_path;
} insp_interfaces__srv__RecognizeInspection_Response;

// Struct for a sequence of insp_interfaces__srv__RecognizeInspection_Response.
typedef struct insp_interfaces__srv__RecognizeInspection_Response__Sequence
{
  insp_interfaces__srv__RecognizeInspection_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} insp_interfaces__srv__RecognizeInspection_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__STRUCT_H_
