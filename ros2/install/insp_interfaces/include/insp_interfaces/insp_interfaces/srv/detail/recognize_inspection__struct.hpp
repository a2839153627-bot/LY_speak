// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__STRUCT_HPP_
#define INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__insp_interfaces__srv__RecognizeInspection_Request __attribute__((deprecated))
#else
# define DEPRECATED__insp_interfaces__srv__RecognizeInspection_Request __declspec(deprecated)
#endif

namespace insp_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct RecognizeInspection_Request_
{
  using Type = RecognizeInspection_Request_<ContainerAllocator>;

  explicit RecognizeInspection_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->algorithm = "";
      this->image_path = "";
      this->output_dir = "";
      this->resource_dir = "";
      this->task_dir = "";
      this->point_id = 0l;
      this->point_name = "";
      this->node_type = "";
    }
  }

  explicit RecognizeInspection_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : algorithm(_alloc),
    image_path(_alloc),
    output_dir(_alloc),
    resource_dir(_alloc),
    task_dir(_alloc),
    point_name(_alloc),
    node_type(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->algorithm = "";
      this->image_path = "";
      this->output_dir = "";
      this->resource_dir = "";
      this->task_dir = "";
      this->point_id = 0l;
      this->point_name = "";
      this->node_type = "";
    }
  }

  // field types and members
  using _algorithm_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _algorithm_type algorithm;
  using _image_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _image_path_type image_path;
  using _output_dir_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _output_dir_type output_dir;
  using _resource_dir_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _resource_dir_type resource_dir;
  using _task_dir_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _task_dir_type task_dir;
  using _point_id_type =
    int32_t;
  _point_id_type point_id;
  using _point_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _point_name_type point_name;
  using _node_type_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _node_type_type node_type;

  // setters for named parameter idiom
  Type & set__algorithm(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->algorithm = _arg;
    return *this;
  }
  Type & set__image_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->image_path = _arg;
    return *this;
  }
  Type & set__output_dir(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->output_dir = _arg;
    return *this;
  }
  Type & set__resource_dir(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->resource_dir = _arg;
    return *this;
  }
  Type & set__task_dir(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->task_dir = _arg;
    return *this;
  }
  Type & set__point_id(
    const int32_t & _arg)
  {
    this->point_id = _arg;
    return *this;
  }
  Type & set__point_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->point_name = _arg;
    return *this;
  }
  Type & set__node_type(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->node_type = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__insp_interfaces__srv__RecognizeInspection_Request
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__insp_interfaces__srv__RecognizeInspection_Request
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RecognizeInspection_Request_ & other) const
  {
    if (this->algorithm != other.algorithm) {
      return false;
    }
    if (this->image_path != other.image_path) {
      return false;
    }
    if (this->output_dir != other.output_dir) {
      return false;
    }
    if (this->resource_dir != other.resource_dir) {
      return false;
    }
    if (this->task_dir != other.task_dir) {
      return false;
    }
    if (this->point_id != other.point_id) {
      return false;
    }
    if (this->point_name != other.point_name) {
      return false;
    }
    if (this->node_type != other.node_type) {
      return false;
    }
    return true;
  }
  bool operator!=(const RecognizeInspection_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RecognizeInspection_Request_

// alias to use template instance with default allocator
using RecognizeInspection_Request =
  insp_interfaces::srv::RecognizeInspection_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace insp_interfaces


#ifndef _WIN32
# define DEPRECATED__insp_interfaces__srv__RecognizeInspection_Response __attribute__((deprecated))
#else
# define DEPRECATED__insp_interfaces__srv__RecognizeInspection_Response __declspec(deprecated)
#endif

namespace insp_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct RecognizeInspection_Response_
{
  using Type = RecognizeInspection_Response_<ContainerAllocator>;

  explicit RecognizeInspection_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->result_json = "";
      this->visualization_path = "";
    }
  }

  explicit RecognizeInspection_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc),
    result_json(_alloc),
    visualization_path(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->result_json = "";
      this->visualization_path = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _result_json_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _result_json_type result_json;
  using _visualization_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _visualization_path_type visualization_path;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__result_json(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->result_json = _arg;
    return *this;
  }
  Type & set__visualization_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->visualization_path = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__insp_interfaces__srv__RecognizeInspection_Response
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__insp_interfaces__srv__RecognizeInspection_Response
    std::shared_ptr<insp_interfaces::srv::RecognizeInspection_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RecognizeInspection_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->result_json != other.result_json) {
      return false;
    }
    if (this->visualization_path != other.visualization_path) {
      return false;
    }
    return true;
  }
  bool operator!=(const RecognizeInspection_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RecognizeInspection_Response_

// alias to use template instance with default allocator
using RecognizeInspection_Response =
  insp_interfaces::srv::RecognizeInspection_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace insp_interfaces

namespace insp_interfaces
{

namespace srv
{

struct RecognizeInspection
{
  using Request = insp_interfaces::srv::RecognizeInspection_Request;
  using Response = insp_interfaces::srv::RecognizeInspection_Response;
};

}  // namespace srv

}  // namespace insp_interfaces

#endif  // INSP_INTERFACES__SRV__DETAIL__RECOGNIZE_INSPECTION__STRUCT_HPP_
