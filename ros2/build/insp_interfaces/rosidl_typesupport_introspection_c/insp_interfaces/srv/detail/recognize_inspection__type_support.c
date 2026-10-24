// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "insp_interfaces/srv/detail/recognize_inspection__rosidl_typesupport_introspection_c.h"
#include "insp_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "insp_interfaces/srv/detail/recognize_inspection__functions.h"
#include "insp_interfaces/srv/detail/recognize_inspection__struct.h"


// Include directives for member types
// Member `algorithm`
// Member `image_path`
// Member `output_dir`
// Member `resource_dir`
// Member `task_dir`
// Member `point_name`
// Member `node_type`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  insp_interfaces__srv__RecognizeInspection_Request__init(message_memory);
}

void insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_fini_function(void * message_memory)
{
  insp_interfaces__srv__RecognizeInspection_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_member_array[8] = {
  {
    "algorithm",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, algorithm),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "image_path",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, image_path),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "output_dir",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, output_dir),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "resource_dir",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, resource_dir),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "task_dir",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, task_dir),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "point_id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, point_id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "point_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, point_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "node_type",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Request, node_type),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_members = {
  "insp_interfaces__srv",  // message namespace
  "RecognizeInspection_Request",  // message name
  8,  // number of fields
  sizeof(insp_interfaces__srv__RecognizeInspection_Request),
  insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_member_array,  // message members
  insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_type_support_handle = {
  0,
  &insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_insp_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection_Request)() {
  if (!insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_type_support_handle.typesupport_identifier) {
    insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &insp_interfaces__srv__RecognizeInspection_Request__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "insp_interfaces/srv/detail/recognize_inspection__rosidl_typesupport_introspection_c.h"
// already included above
// #include "insp_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "insp_interfaces/srv/detail/recognize_inspection__functions.h"
// already included above
// #include "insp_interfaces/srv/detail/recognize_inspection__struct.h"


// Include directives for member types
// Member `message`
// Member `result_json`
// Member `visualization_path`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  insp_interfaces__srv__RecognizeInspection_Response__init(message_memory);
}

void insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_fini_function(void * message_memory)
{
  insp_interfaces__srv__RecognizeInspection_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_member_array[4] = {
  {
    "success",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Response, success),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "message",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Response, message),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result_json",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Response, result_json),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "visualization_path",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(insp_interfaces__srv__RecognizeInspection_Response, visualization_path),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_members = {
  "insp_interfaces__srv",  // message namespace
  "RecognizeInspection_Response",  // message name
  4,  // number of fields
  sizeof(insp_interfaces__srv__RecognizeInspection_Response),
  insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_member_array,  // message members
  insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_type_support_handle = {
  0,
  &insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_insp_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection_Response)() {
  if (!insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_type_support_handle.typesupport_identifier) {
    insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &insp_interfaces__srv__RecognizeInspection_Response__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "insp_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "insp_interfaces/srv/detail/recognize_inspection__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_members = {
  "insp_interfaces__srv",  // service namespace
  "RecognizeInspection",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_Request_message_type_support_handle,
  NULL  // response message
  // insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_Response_message_type_support_handle
};

static rosidl_service_type_support_t insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_type_support_handle = {
  0,
  &insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_insp_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection)() {
  if (!insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_type_support_handle.typesupport_identifier) {
    insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, insp_interfaces, srv, RecognizeInspection_Response)()->data;
  }

  return &insp_interfaces__srv__detail__recognize_inspection__rosidl_typesupport_introspection_c__RecognizeInspection_service_type_support_handle;
}
