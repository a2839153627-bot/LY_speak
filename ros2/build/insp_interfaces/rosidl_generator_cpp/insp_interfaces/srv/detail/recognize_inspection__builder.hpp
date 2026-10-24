// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__BUILDER_HPP_
#define INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "insp_interfaces/srv/detail/recognize_inspection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace insp_interfaces
{

namespace srv
{

namespace builder
{

class Init_RecognizeInspection_Request_node_type
{
public:
  explicit Init_RecognizeInspection_Request_node_type(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  ::insp_interfaces::srv::RecognizeInspection_Request node_type(::insp_interfaces::srv::RecognizeInspection_Request::_node_type_type arg)
  {
    msg_.node_type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_point_name
{
public:
  explicit Init_RecognizeInspection_Request_point_name(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Request_node_type point_name(::insp_interfaces::srv::RecognizeInspection_Request::_point_name_type arg)
  {
    msg_.point_name = std::move(arg);
    return Init_RecognizeInspection_Request_node_type(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_point_id
{
public:
  explicit Init_RecognizeInspection_Request_point_id(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Request_point_name point_id(::insp_interfaces::srv::RecognizeInspection_Request::_point_id_type arg)
  {
    msg_.point_id = std::move(arg);
    return Init_RecognizeInspection_Request_point_name(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_task_dir
{
public:
  explicit Init_RecognizeInspection_Request_task_dir(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Request_point_id task_dir(::insp_interfaces::srv::RecognizeInspection_Request::_task_dir_type arg)
  {
    msg_.task_dir = std::move(arg);
    return Init_RecognizeInspection_Request_point_id(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_resource_dir
{
public:
  explicit Init_RecognizeInspection_Request_resource_dir(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Request_task_dir resource_dir(::insp_interfaces::srv::RecognizeInspection_Request::_resource_dir_type arg)
  {
    msg_.resource_dir = std::move(arg);
    return Init_RecognizeInspection_Request_task_dir(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_output_dir
{
public:
  explicit Init_RecognizeInspection_Request_output_dir(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Request_resource_dir output_dir(::insp_interfaces::srv::RecognizeInspection_Request::_output_dir_type arg)
  {
    msg_.output_dir = std::move(arg);
    return Init_RecognizeInspection_Request_resource_dir(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_image_path
{
public:
  explicit Init_RecognizeInspection_Request_image_path(::insp_interfaces::srv::RecognizeInspection_Request & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Request_output_dir image_path(::insp_interfaces::srv::RecognizeInspection_Request::_image_path_type arg)
  {
    msg_.image_path = std::move(arg);
    return Init_RecognizeInspection_Request_output_dir(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

class Init_RecognizeInspection_Request_algorithm
{
public:
  Init_RecognizeInspection_Request_algorithm()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RecognizeInspection_Request_image_path algorithm(::insp_interfaces::srv::RecognizeInspection_Request::_algorithm_type arg)
  {
    msg_.algorithm = std::move(arg);
    return Init_RecognizeInspection_Request_image_path(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::insp_interfaces::srv::RecognizeInspection_Request>()
{
  return insp_interfaces::srv::builder::Init_RecognizeInspection_Request_algorithm();
}

}  // namespace insp_interfaces


namespace insp_interfaces
{

namespace srv
{

namespace builder
{

class Init_RecognizeInspection_Response_visualization_path
{
public:
  explicit Init_RecognizeInspection_Response_visualization_path(::insp_interfaces::srv::RecognizeInspection_Response & msg)
  : msg_(msg)
  {}
  ::insp_interfaces::srv::RecognizeInspection_Response visualization_path(::insp_interfaces::srv::RecognizeInspection_Response::_visualization_path_type arg)
  {
    msg_.visualization_path = std::move(arg);
    return std::move(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Response msg_;
};

class Init_RecognizeInspection_Response_result_json
{
public:
  explicit Init_RecognizeInspection_Response_result_json(::insp_interfaces::srv::RecognizeInspection_Response & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Response_visualization_path result_json(::insp_interfaces::srv::RecognizeInspection_Response::_result_json_type arg)
  {
    msg_.result_json = std::move(arg);
    return Init_RecognizeInspection_Response_visualization_path(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Response msg_;
};

class Init_RecognizeInspection_Response_message
{
public:
  explicit Init_RecognizeInspection_Response_message(::insp_interfaces::srv::RecognizeInspection_Response & msg)
  : msg_(msg)
  {}
  Init_RecognizeInspection_Response_result_json message(::insp_interfaces::srv::RecognizeInspection_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_RecognizeInspection_Response_result_json(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Response msg_;
};

class Init_RecognizeInspection_Response_success
{
public:
  Init_RecognizeInspection_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RecognizeInspection_Response_message success(::insp_interfaces::srv::RecognizeInspection_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_RecognizeInspection_Response_message(msg_);
  }

private:
  ::insp_interfaces::srv::RecognizeInspection_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::insp_interfaces::srv::RecognizeInspection_Response>()
{
  return insp_interfaces::srv::builder::Init_RecognizeInspection_Response_success();
}

}  // namespace insp_interfaces

#endif  // INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__BUILDER_HPP_
