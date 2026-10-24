// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice
#include "insp_interfaces/srv/detail/recognize_inspection__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "insp_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "insp_interfaces/srv/detail/recognize_inspection__struct.h"
#include "insp_interfaces/srv/detail/recognize_inspection__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // algorithm, image_path, node_type, output_dir, point_name, resource_dir, task_dir
#include "rosidl_runtime_c/string_functions.h"  // algorithm, image_path, node_type, output_dir, point_name, resource_dir, task_dir

// forward declare type support functions


using _RecognizeInspection_Request__ros_msg_type = insp_interfaces__srv__RecognizeInspection_Request;

static bool _RecognizeInspection_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _RecognizeInspection_Request__ros_msg_type * ros_message = static_cast<const _RecognizeInspection_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: algorithm
  {
    const rosidl_runtime_c__String * str = &ros_message->algorithm;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: image_path
  {
    const rosidl_runtime_c__String * str = &ros_message->image_path;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: output_dir
  {
    const rosidl_runtime_c__String * str = &ros_message->output_dir;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: resource_dir
  {
    const rosidl_runtime_c__String * str = &ros_message->resource_dir;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: task_dir
  {
    const rosidl_runtime_c__String * str = &ros_message->task_dir;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: point_id
  {
    cdr << ros_message->point_id;
  }

  // Field name: point_name
  {
    const rosidl_runtime_c__String * str = &ros_message->point_name;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: node_type
  {
    const rosidl_runtime_c__String * str = &ros_message->node_type;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _RecognizeInspection_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _RecognizeInspection_Request__ros_msg_type * ros_message = static_cast<_RecognizeInspection_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: algorithm
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->algorithm.data) {
      rosidl_runtime_c__String__init(&ros_message->algorithm);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->algorithm,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'algorithm'\n");
      return false;
    }
  }

  // Field name: image_path
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->image_path.data) {
      rosidl_runtime_c__String__init(&ros_message->image_path);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->image_path,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'image_path'\n");
      return false;
    }
  }

  // Field name: output_dir
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->output_dir.data) {
      rosidl_runtime_c__String__init(&ros_message->output_dir);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->output_dir,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'output_dir'\n");
      return false;
    }
  }

  // Field name: resource_dir
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->resource_dir.data) {
      rosidl_runtime_c__String__init(&ros_message->resource_dir);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->resource_dir,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'resource_dir'\n");
      return false;
    }
  }

  // Field name: task_dir
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->task_dir.data) {
      rosidl_runtime_c__String__init(&ros_message->task_dir);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->task_dir,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'task_dir'\n");
      return false;
    }
  }

  // Field name: point_id
  {
    cdr >> ros_message->point_id;
  }

  // Field name: point_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->point_name.data) {
      rosidl_runtime_c__String__init(&ros_message->point_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->point_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'point_name'\n");
      return false;
    }
  }

  // Field name: node_type
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->node_type.data) {
      rosidl_runtime_c__String__init(&ros_message->node_type);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->node_type,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'node_type'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_insp_interfaces
size_t get_serialized_size_insp_interfaces__srv__RecognizeInspection_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _RecognizeInspection_Request__ros_msg_type * ros_message = static_cast<const _RecognizeInspection_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name algorithm
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->algorithm.size + 1);
  // field.name image_path
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->image_path.size + 1);
  // field.name output_dir
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->output_dir.size + 1);
  // field.name resource_dir
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->resource_dir.size + 1);
  // field.name task_dir
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->task_dir.size + 1);
  // field.name point_id
  {
    size_t item_size = sizeof(ros_message->point_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name point_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->point_name.size + 1);
  // field.name node_type
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->node_type.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _RecognizeInspection_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_insp_interfaces__srv__RecognizeInspection_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_insp_interfaces
size_t max_serialized_size_insp_interfaces__srv__RecognizeInspection_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: algorithm
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: image_path
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: output_dir
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: resource_dir
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: task_dir
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: point_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: point_name
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: node_type
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = insp_interfaces__srv__RecognizeInspection_Request;
    is_plain =
      (
      offsetof(DataType, node_type) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _RecognizeInspection_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_insp_interfaces__srv__RecognizeInspection_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_RecognizeInspection_Request = {
  "insp_interfaces::srv",
  "RecognizeInspection_Request",
  _RecognizeInspection_Request__cdr_serialize,
  _RecognizeInspection_Request__cdr_deserialize,
  _RecognizeInspection_Request__get_serialized_size,
  _RecognizeInspection_Request__max_serialized_size
};

static rosidl_message_type_support_t _RecognizeInspection_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_RecognizeInspection_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, insp_interfaces, srv, RecognizeInspection_Request)() {
  return &_RecognizeInspection_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "insp_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "insp_interfaces/srv/detail/recognize_inspection__struct.h"
// already included above
// #include "insp_interfaces/srv/detail/recognize_inspection__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // message, result_json, visualization_path
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // message, result_json, visualization_path

// forward declare type support functions


using _RecognizeInspection_Response__ros_msg_type = insp_interfaces__srv__RecognizeInspection_Response;

static bool _RecognizeInspection_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _RecognizeInspection_Response__ros_msg_type * ros_message = static_cast<const _RecognizeInspection_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: message
  {
    const rosidl_runtime_c__String * str = &ros_message->message;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: result_json
  {
    const rosidl_runtime_c__String * str = &ros_message->result_json;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: visualization_path
  {
    const rosidl_runtime_c__String * str = &ros_message->visualization_path;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _RecognizeInspection_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _RecognizeInspection_Response__ros_msg_type * ros_message = static_cast<_RecognizeInspection_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: message
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->message.data) {
      rosidl_runtime_c__String__init(&ros_message->message);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->message,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'message'\n");
      return false;
    }
  }

  // Field name: result_json
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->result_json.data) {
      rosidl_runtime_c__String__init(&ros_message->result_json);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->result_json,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'result_json'\n");
      return false;
    }
  }

  // Field name: visualization_path
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->visualization_path.data) {
      rosidl_runtime_c__String__init(&ros_message->visualization_path);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->visualization_path,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'visualization_path'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_insp_interfaces
size_t get_serialized_size_insp_interfaces__srv__RecognizeInspection_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _RecognizeInspection_Response__ros_msg_type * ros_message = static_cast<const _RecognizeInspection_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->message.size + 1);
  // field.name result_json
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->result_json.size + 1);
  // field.name visualization_path
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->visualization_path.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _RecognizeInspection_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_insp_interfaces__srv__RecognizeInspection_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_insp_interfaces
size_t max_serialized_size_insp_interfaces__srv__RecognizeInspection_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: message
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: result_json
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: visualization_path
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = insp_interfaces__srv__RecognizeInspection_Response;
    is_plain =
      (
      offsetof(DataType, visualization_path) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _RecognizeInspection_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_insp_interfaces__srv__RecognizeInspection_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_RecognizeInspection_Response = {
  "insp_interfaces::srv",
  "RecognizeInspection_Response",
  _RecognizeInspection_Response__cdr_serialize,
  _RecognizeInspection_Response__cdr_deserialize,
  _RecognizeInspection_Response__get_serialized_size,
  _RecognizeInspection_Response__max_serialized_size
};

static rosidl_message_type_support_t _RecognizeInspection_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_RecognizeInspection_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, insp_interfaces, srv, RecognizeInspection_Response)() {
  return &_RecognizeInspection_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "insp_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "insp_interfaces/srv/recognize_inspection.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t RecognizeInspection__callbacks = {
  "insp_interfaces::srv",
  "RecognizeInspection",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, insp_interfaces, srv, RecognizeInspection_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, insp_interfaces, srv, RecognizeInspection_Response)(),
};

static rosidl_service_type_support_t RecognizeInspection__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &RecognizeInspection__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, insp_interfaces, srv, RecognizeInspection)() {
  return &RecognizeInspection__handle;
}

#if defined(__cplusplus)
}
#endif
