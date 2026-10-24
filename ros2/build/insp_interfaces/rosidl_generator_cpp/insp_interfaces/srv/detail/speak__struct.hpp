// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from insp_interfaces:srv/Speak.idl
// generated code does not contain a copyright notice

#ifndef INSP_INTERFACES__SRV__DETAIL__SPEAK__STRUCT_HPP_
#define INSP_INTERFACES__SRV__DETAIL__SPEAK__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__insp_interfaces__srv__Speak_Request __attribute__((deprecated))
#else
# define DEPRECATED__insp_interfaces__srv__Speak_Request __declspec(deprecated)
#endif

namespace insp_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Speak_Request_
{
  using Type = Speak_Request_<ContainerAllocator>;

  explicit Speak_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->text = "";
      this->interrupt_current = false;
    }
  }

  explicit Speak_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : text(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->text = "";
      this->interrupt_current = false;
    }
  }

  // field types and members
  using _text_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _text_type text;
  using _interrupt_current_type =
    bool;
  _interrupt_current_type interrupt_current;

  // setters for named parameter idiom
  Type & set__text(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->text = _arg;
    return *this;
  }
  Type & set__interrupt_current(
    const bool & _arg)
  {
    this->interrupt_current = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    insp_interfaces::srv::Speak_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const insp_interfaces::srv::Speak_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::Speak_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::Speak_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__insp_interfaces__srv__Speak_Request
    std::shared_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__insp_interfaces__srv__Speak_Request
    std::shared_ptr<insp_interfaces::srv::Speak_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Speak_Request_ & other) const
  {
    if (this->text != other.text) {
      return false;
    }
    if (this->interrupt_current != other.interrupt_current) {
      return false;
    }
    return true;
  }
  bool operator!=(const Speak_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Speak_Request_

// alias to use template instance with default allocator
using Speak_Request =
  insp_interfaces::srv::Speak_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace insp_interfaces


#ifndef _WIN32
# define DEPRECATED__insp_interfaces__srv__Speak_Response __attribute__((deprecated))
#else
# define DEPRECATED__insp_interfaces__srv__Speak_Response __declspec(deprecated)
#endif

namespace insp_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Speak_Response_
{
  using Type = Speak_Response_<ContainerAllocator>;

  explicit Speak_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
      this->message = "";
    }
  }

  explicit Speak_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->accepted = false;
      this->message = "";
    }
  }

  // field types and members
  using _accepted_type =
    bool;
  _accepted_type accepted;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__accepted(
    const bool & _arg)
  {
    this->accepted = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    insp_interfaces::srv::Speak_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const insp_interfaces::srv::Speak_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::Speak_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      insp_interfaces::srv::Speak_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__insp_interfaces__srv__Speak_Response
    std::shared_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__insp_interfaces__srv__Speak_Response
    std::shared_ptr<insp_interfaces::srv::Speak_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Speak_Response_ & other) const
  {
    if (this->accepted != other.accepted) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const Speak_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Speak_Response_

// alias to use template instance with default allocator
using Speak_Response =
  insp_interfaces::srv::Speak_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace insp_interfaces

namespace insp_interfaces
{

namespace srv
{

struct Speak
{
  using Request = insp_interfaces::srv::Speak_Request;
  using Response = insp_interfaces::srv::Speak_Response;
};

}  // namespace srv

}  // namespace insp_interfaces

#endif  // INSP_INTERFACES__SRV__DETAIL__SPEAK__STRUCT_HPP_
