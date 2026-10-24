// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__TRAITS_HPP_
#define INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "insp_interfaces/srv/detail/recognize_inspection__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace insp_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const RecognizeInspection_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: algorithm
  {
    out << "algorithm: ";
    rosidl_generator_traits::value_to_yaml(msg.algorithm, out);
    out << ", ";
  }

  // member: image_path
  {
    out << "image_path: ";
    rosidl_generator_traits::value_to_yaml(msg.image_path, out);
    out << ", ";
  }

  // member: output_dir
  {
    out << "output_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.output_dir, out);
    out << ", ";
  }

  // member: resource_dir
  {
    out << "resource_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.resource_dir, out);
    out << ", ";
  }

  // member: task_dir
  {
    out << "task_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.task_dir, out);
    out << ", ";
  }

  // member: point_id
  {
    out << "point_id: ";
    rosidl_generator_traits::value_to_yaml(msg.point_id, out);
    out << ", ";
  }

  // member: point_name
  {
    out << "point_name: ";
    rosidl_generator_traits::value_to_yaml(msg.point_name, out);
    out << ", ";
  }

  // member: node_type
  {
    out << "node_type: ";
    rosidl_generator_traits::value_to_yaml(msg.node_type, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RecognizeInspection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: algorithm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "algorithm: ";
    rosidl_generator_traits::value_to_yaml(msg.algorithm, out);
    out << "\n";
  }

  // member: image_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "image_path: ";
    rosidl_generator_traits::value_to_yaml(msg.image_path, out);
    out << "\n";
  }

  // member: output_dir
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "output_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.output_dir, out);
    out << "\n";
  }

  // member: resource_dir
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "resource_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.resource_dir, out);
    out << "\n";
  }

  // member: task_dir
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "task_dir: ";
    rosidl_generator_traits::value_to_yaml(msg.task_dir, out);
    out << "\n";
  }

  // member: point_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point_id: ";
    rosidl_generator_traits::value_to_yaml(msg.point_id, out);
    out << "\n";
  }

  // member: point_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "point_name: ";
    rosidl_generator_traits::value_to_yaml(msg.point_name, out);
    out << "\n";
  }

  // member: node_type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "node_type: ";
    rosidl_generator_traits::value_to_yaml(msg.node_type, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RecognizeInspection_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace insp_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use insp_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const insp_interfaces::srv::RecognizeInspection_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  insp_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use insp_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const insp_interfaces::srv::RecognizeInspection_Request & msg)
{
  return insp_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<insp_interfaces::srv::RecognizeInspection_Request>()
{
  return "insp_interfaces::srv::RecognizeInspection_Request";
}

template<>
inline const char * name<insp_interfaces::srv::RecognizeInspection_Request>()
{
  return "insp_interfaces/srv/RecognizeInspection_Request";
}

template<>
struct has_fixed_size<insp_interfaces::srv::RecognizeInspection_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<insp_interfaces::srv::RecognizeInspection_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<insp_interfaces::srv::RecognizeInspection_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace insp_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const RecognizeInspection_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: result_json
  {
    out << "result_json: ";
    rosidl_generator_traits::value_to_yaml(msg.result_json, out);
    out << ", ";
  }

  // member: visualization_path
  {
    out << "visualization_path: ";
    rosidl_generator_traits::value_to_yaml(msg.visualization_path, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const RecognizeInspection_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }

  // member: result_json
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result_json: ";
    rosidl_generator_traits::value_to_yaml(msg.result_json, out);
    out << "\n";
  }

  // member: visualization_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "visualization_path: ";
    rosidl_generator_traits::value_to_yaml(msg.visualization_path, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const RecognizeInspection_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace insp_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use insp_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const insp_interfaces::srv::RecognizeInspection_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  insp_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use insp_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const insp_interfaces::srv::RecognizeInspection_Response & msg)
{
  return insp_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<insp_interfaces::srv::RecognizeInspection_Response>()
{
  return "insp_interfaces::srv::RecognizeInspection_Response";
}

template<>
inline const char * name<insp_interfaces::srv::RecognizeInspection_Response>()
{
  return "insp_interfaces/srv/RecognizeInspection_Response";
}

template<>
struct has_fixed_size<insp_interfaces::srv::RecognizeInspection_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<insp_interfaces::srv::RecognizeInspection_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<insp_interfaces::srv::RecognizeInspection_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<insp_interfaces::srv::RecognizeInspection>()
{
  return "insp_interfaces::srv::RecognizeInspection";
}

template<>
inline const char * name<insp_interfaces::srv::RecognizeInspection>()
{
  return "insp_interfaces/srv/RecognizeInspection";
}

template<>
struct has_fixed_size<insp_interfaces::srv::RecognizeInspection>
  : std::integral_constant<
    bool,
    has_fixed_size<insp_interfaces::srv::RecognizeInspection_Request>::value &&
    has_fixed_size<insp_interfaces::srv::RecognizeInspection_Response>::value
  >
{
};

template<>
struct has_bounded_size<insp_interfaces::srv::RecognizeInspection>
  : std::integral_constant<
    bool,
    has_bounded_size<insp_interfaces::srv::RecognizeInspection_Request>::value &&
    has_bounded_size<insp_interfaces::srv::RecognizeInspection_Response>::value
  >
{
};

template<>
struct is_service<insp_interfaces::srv::RecognizeInspection>
  : std::true_type
{
};

template<>
struct is_service_request<insp_interfaces::srv::RecognizeInspection_Request>
  : std::true_type
{
};

template<>
struct is_service_response<insp_interfaces::srv::RecognizeInspection_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__TRAITS_HPP_
