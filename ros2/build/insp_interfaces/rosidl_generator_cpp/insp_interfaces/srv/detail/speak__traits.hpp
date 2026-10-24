// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from insp_interfaces:srv/Speak.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__SPEAK__TRAITS_HPP_
#define INSP_INTERFACES__SRV__DETAIL__SPEAK__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "insp_interfaces/srv/detail/speak__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace insp_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Speak_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: text
  {
    out << "text: ";
    rosidl_generator_traits::value_to_yaml(msg.text, out);
    out << ", ";
  }

  // member: interrupt_current
  {
    out << "interrupt_current: ";
    rosidl_generator_traits::value_to_yaml(msg.interrupt_current, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Speak_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: text
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "text: ";
    rosidl_generator_traits::value_to_yaml(msg.text, out);
    out << "\n";
  }

  // member: interrupt_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "interrupt_current: ";
    rosidl_generator_traits::value_to_yaml(msg.interrupt_current, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Speak_Request & msg, bool use_flow_style = false)
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
  const insp_interfaces::srv::Speak_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  insp_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use insp_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const insp_interfaces::srv::Speak_Request & msg)
{
  return insp_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<insp_interfaces::srv::Speak_Request>()
{
  return "insp_interfaces::srv::Speak_Request";
}

template<>
inline const char * name<insp_interfaces::srv::Speak_Request>()
{
  return "insp_interfaces/srv/Speak_Request";
}

template<>
struct has_fixed_size<insp_interfaces::srv::Speak_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<insp_interfaces::srv::Speak_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<insp_interfaces::srv::Speak_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace insp_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Speak_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Speak_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Speak_Response & msg, bool use_flow_style = false)
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
  const insp_interfaces::srv::Speak_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  insp_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use insp_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const insp_interfaces::srv::Speak_Response & msg)
{
  return insp_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<insp_interfaces::srv::Speak_Response>()
{
  return "insp_interfaces::srv::Speak_Response";
}

template<>
inline const char * name<insp_interfaces::srv::Speak_Response>()
{
  return "insp_interfaces/srv/Speak_Response";
}

template<>
struct has_fixed_size<insp_interfaces::srv::Speak_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<insp_interfaces::srv::Speak_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<insp_interfaces::srv::Speak_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<insp_interfaces::srv::Speak>()
{
  return "insp_interfaces::srv::Speak";
}

template<>
inline const char * name<insp_interfaces::srv::Speak>()
{
  return "insp_interfaces/srv/Speak";
}

template<>
struct has_fixed_size<insp_interfaces::srv::Speak>
  : std::integral_constant<
    bool,
    has_fixed_size<insp_interfaces::srv::Speak_Request>::value &&
    has_fixed_size<insp_interfaces::srv::Speak_Response>::value
  >
{
};

template<>
struct has_bounded_size<insp_interfaces::srv::Speak>
  : std::integral_constant<
    bool,
    has_bounded_size<insp_interfaces::srv::Speak_Request>::value &&
    has_bounded_size<insp_interfaces::srv::Speak_Response>::value
  >
{
};

template<>
struct is_service<insp_interfaces::srv::Speak>
  : std::true_type
{
};

template<>
struct is_service_request<insp_interfaces::srv::Speak_Request>
  : std::true_type
{
};

template<>
struct is_service_response<insp_interfaces::srv::Speak_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // INSP_INTERFACES__SRV__DETAIL__SPEAK__TRAITS_HPP_
