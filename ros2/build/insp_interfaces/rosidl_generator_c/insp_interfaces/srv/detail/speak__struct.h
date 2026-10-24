// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from insp_interfaces:srv/Speak.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__SPEAK__STRUCT_H_
#define INSP_INTERFACES__SRV__DETAIL__SPEAK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'text'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Speak in the package insp_interfaces.
typedef struct insp_interfaces__srv__Speak_Request
{
  rosidl_runtime_c__String text;
  bool interrupt_current;
} insp_interfaces__srv__Speak_Request;

// Struct for a sequence of insp_interfaces__srv__Speak_Request.
typedef struct insp_interfaces__srv__Speak_Request__Sequence
{
  insp_interfaces__srv__Speak_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} insp_interfaces__srv__Speak_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Speak in the package insp_interfaces.
typedef struct insp_interfaces__srv__Speak_Response
{
  bool accepted;
  rosidl_runtime_c__String message;
} insp_interfaces__srv__Speak_Response;

// Struct for a sequence of insp_interfaces__srv__Speak_Response.
typedef struct insp_interfaces__srv__Speak_Response__Sequence
{
  insp_interfaces__srv__Speak_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} insp_interfaces__srv__Speak_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INSP_INTERFACES__SRV__DETAIL__SPEAK__STRUCT_H_
