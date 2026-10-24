// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from insp_interfaces:srv/Speak.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__SPEAK__BUILDER_HPP_
#define INSP_INTERFACES__SRV__DETAIL__SPEAK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "insp_interfaces/srv/detail/speak__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace insp_interfaces
{

namespace srv
{

namespace builder
{

class Init_Speak_Request_interrupt_current
{
public:
  explicit Init_Speak_Request_interrupt_current(::insp_interfaces::srv::Speak_Request & msg)
  : msg_(msg)
  {}
  ::insp_interfaces::srv::Speak_Request interrupt_current(::insp_interfaces::srv::Speak_Request::_interrupt_current_type arg)
  {
    msg_.interrupt_current = std::move(arg);
    return std::move(msg_);
  }

private:
  ::insp_interfaces::srv::Speak_Request msg_;
};

class Init_Speak_Request_text
{
public:
  Init_Speak_Request_text()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Speak_Request_interrupt_current text(::insp_interfaces::srv::Speak_Request::_text_type arg)
  {
    msg_.text = std::move(arg);
    return Init_Speak_Request_interrupt_current(msg_);
  }

private:
  ::insp_interfaces::srv::Speak_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::insp_interfaces::srv::Speak_Request>()
{
  return insp_interfaces::srv::builder::Init_Speak_Request_text();
}

}  // namespace insp_interfaces


namespace insp_interfaces
{

namespace srv
{

namespace builder
{

class Init_Speak_Response_message
{
public:
  explicit Init_Speak_Response_message(::insp_interfaces::srv::Speak_Response & msg)
  : msg_(msg)
  {}
  ::insp_interfaces::srv::Speak_Response message(::insp_interfaces::srv::Speak_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::insp_interfaces::srv::Speak_Response msg_;
};

class Init_Speak_Response_accepted
{
public:
  Init_Speak_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Speak_Response_message accepted(::insp_interfaces::srv::Speak_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Speak_Response_message(msg_);
  }

private:
  ::insp_interfaces::srv::Speak_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::insp_interfaces::srv::Speak_Response>()
{
  return insp_interfaces::srv::builder::Init_Speak_Response_accepted();
}

}  // namespace insp_interfaces

#endif  // INSP_INTERFACES__SRV__DETAIL__SPEAK__BUILDER_HPP_
