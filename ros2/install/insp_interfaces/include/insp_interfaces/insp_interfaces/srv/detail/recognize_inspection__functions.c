// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from insp_interfaces:srv/RecognizeInspection.idl
// generated code does not contain a copyright notice
#include "insp_interfaces/srv/detail/recognize_inspection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `algorithm`
// Member `image_path`
// Member `output_dir`
// Member `resource_dir`
// Member `task_dir`
// Member `point_name`
// Member `node_type`
#include "rosidl_runtime_c/string_functions.h"

bool
insp_interfaces__srv__RecognizeInspection_Request__init(insp_interfaces__srv__RecognizeInspection_Request * msg)
{
  if (!msg) {
    return false;
  }
  // algorithm
  if (!rosidl_runtime_c__String__init(&msg->algorithm)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  // image_path
  if (!rosidl_runtime_c__String__init(&msg->image_path)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  // output_dir
  if (!rosidl_runtime_c__String__init(&msg->output_dir)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  // resource_dir
  if (!rosidl_runtime_c__String__init(&msg->resource_dir)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  // task_dir
  if (!rosidl_runtime_c__String__init(&msg->task_dir)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  // point_id
  // point_name
  if (!rosidl_runtime_c__String__init(&msg->point_name)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  // node_type
  if (!rosidl_runtime_c__String__init(&msg->node_type)) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
    return false;
  }
  return true;
}

void
insp_interfaces__srv__RecognizeInspection_Request__fini(insp_interfaces__srv__RecognizeInspection_Request * msg)
{
  if (!msg) {
    return;
  }
  // algorithm
  rosidl_runtime_c__String__fini(&msg->algorithm);
  // image_path
  rosidl_runtime_c__String__fini(&msg->image_path);
  // output_dir
  rosidl_runtime_c__String__fini(&msg->output_dir);
  // resource_dir
  rosidl_runtime_c__String__fini(&msg->resource_dir);
  // task_dir
  rosidl_runtime_c__String__fini(&msg->task_dir);
  // point_id
  // point_name
  rosidl_runtime_c__String__fini(&msg->point_name);
  // node_type
  rosidl_runtime_c__String__fini(&msg->node_type);
}

bool
insp_interfaces__srv__RecognizeInspection_Request__are_equal(const insp_interfaces__srv__RecognizeInspection_Request * lhs, const insp_interfaces__srv__RecognizeInspection_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // algorithm
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->algorithm), &(rhs->algorithm)))
  {
    return false;
  }
  // image_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->image_path), &(rhs->image_path)))
  {
    return false;
  }
  // output_dir
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->output_dir), &(rhs->output_dir)))
  {
    return false;
  }
  // resource_dir
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->resource_dir), &(rhs->resource_dir)))
  {
    return false;
  }
  // task_dir
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->task_dir), &(rhs->task_dir)))
  {
    return false;
  }
  // point_id
  if (lhs->point_id != rhs->point_id) {
    return false;
  }
  // point_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->point_name), &(rhs->point_name)))
  {
    return false;
  }
  // node_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->node_type), &(rhs->node_type)))
  {
    return false;
  }
  return true;
}

bool
insp_interfaces__srv__RecognizeInspection_Request__copy(
  const insp_interfaces__srv__RecognizeInspection_Request * input,
  insp_interfaces__srv__RecognizeInspection_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // algorithm
  if (!rosidl_runtime_c__String__copy(
      &(input->algorithm), &(output->algorithm)))
  {
    return false;
  }
  // image_path
  if (!rosidl_runtime_c__String__copy(
      &(input->image_path), &(output->image_path)))
  {
    return false;
  }
  // output_dir
  if (!rosidl_runtime_c__String__copy(
      &(input->output_dir), &(output->output_dir)))
  {
    return false;
  }
  // resource_dir
  if (!rosidl_runtime_c__String__copy(
      &(input->resource_dir), &(output->resource_dir)))
  {
    return false;
  }
  // task_dir
  if (!rosidl_runtime_c__String__copy(
      &(input->task_dir), &(output->task_dir)))
  {
    return false;
  }
  // point_id
  output->point_id = input->point_id;
  // point_name
  if (!rosidl_runtime_c__String__copy(
      &(input->point_name), &(output->point_name)))
  {
    return false;
  }
  // node_type
  if (!rosidl_runtime_c__String__copy(
      &(input->node_type), &(output->node_type)))
  {
    return false;
  }
  return true;
}

insp_interfaces__srv__RecognizeInspection_Request *
insp_interfaces__srv__RecognizeInspection_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__RecognizeInspection_Request * msg = (insp_interfaces__srv__RecognizeInspection_Request *)allocator.allocate(sizeof(insp_interfaces__srv__RecognizeInspection_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(insp_interfaces__srv__RecognizeInspection_Request));
  bool success = insp_interfaces__srv__RecognizeInspection_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
insp_interfaces__srv__RecognizeInspection_Request__destroy(insp_interfaces__srv__RecognizeInspection_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    insp_interfaces__srv__RecognizeInspection_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
insp_interfaces__srv__RecognizeInspection_Request__Sequence__init(insp_interfaces__srv__RecognizeInspection_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__RecognizeInspection_Request * data = NULL;

  if (size) {
    data = (insp_interfaces__srv__RecognizeInspection_Request *)allocator.zero_allocate(size, sizeof(insp_interfaces__srv__RecognizeInspection_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = insp_interfaces__srv__RecognizeInspection_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        insp_interfaces__srv__RecognizeInspection_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
insp_interfaces__srv__RecognizeInspection_Request__Sequence__fini(insp_interfaces__srv__RecognizeInspection_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      insp_interfaces__srv__RecognizeInspection_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

insp_interfaces__srv__RecognizeInspection_Request__Sequence *
insp_interfaces__srv__RecognizeInspection_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__RecognizeInspection_Request__Sequence * array = (insp_interfaces__srv__RecognizeInspection_Request__Sequence *)allocator.allocate(sizeof(insp_interfaces__srv__RecognizeInspection_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = insp_interfaces__srv__RecognizeInspection_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
insp_interfaces__srv__RecognizeInspection_Request__Sequence__destroy(insp_interfaces__srv__RecognizeInspection_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    insp_interfaces__srv__RecognizeInspection_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
insp_interfaces__srv__RecognizeInspection_Request__Sequence__are_equal(const insp_interfaces__srv__RecognizeInspection_Request__Sequence * lhs, const insp_interfaces__srv__RecognizeInspection_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!insp_interfaces__srv__RecognizeInspection_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
insp_interfaces__srv__RecognizeInspection_Request__Sequence__copy(
  const insp_interfaces__srv__RecognizeInspection_Request__Sequence * input,
  insp_interfaces__srv__RecognizeInspection_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(insp_interfaces__srv__RecognizeInspection_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    insp_interfaces__srv__RecognizeInspection_Request * data =
      (insp_interfaces__srv__RecognizeInspection_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!insp_interfaces__srv__RecognizeInspection_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          insp_interfaces__srv__RecognizeInspection_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!insp_interfaces__srv__RecognizeInspection_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// Member `result_json`
// Member `visualization_path`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
insp_interfaces__srv__RecognizeInspection_Response__init(insp_interfaces__srv__RecognizeInspection_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    insp_interfaces__srv__RecognizeInspection_Response__fini(msg);
    return false;
  }
  // result_json
  if (!rosidl_runtime_c__String__init(&msg->result_json)) {
    insp_interfaces__srv__RecognizeInspection_Response__fini(msg);
    return false;
  }
  // visualization_path
  if (!rosidl_runtime_c__String__init(&msg->visualization_path)) {
    insp_interfaces__srv__RecognizeInspection_Response__fini(msg);
    return false;
  }
  return true;
}

void
insp_interfaces__srv__RecognizeInspection_Response__fini(insp_interfaces__srv__RecognizeInspection_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // result_json
  rosidl_runtime_c__String__fini(&msg->result_json);
  // visualization_path
  rosidl_runtime_c__String__fini(&msg->visualization_path);
}

bool
insp_interfaces__srv__RecognizeInspection_Response__are_equal(const insp_interfaces__srv__RecognizeInspection_Response * lhs, const insp_interfaces__srv__RecognizeInspection_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  // result_json
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->result_json), &(rhs->result_json)))
  {
    return false;
  }
  // visualization_path
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->visualization_path), &(rhs->visualization_path)))
  {
    return false;
  }
  return true;
}

bool
insp_interfaces__srv__RecognizeInspection_Response__copy(
  const insp_interfaces__srv__RecognizeInspection_Response * input,
  insp_interfaces__srv__RecognizeInspection_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  // result_json
  if (!rosidl_runtime_c__String__copy(
      &(input->result_json), &(output->result_json)))
  {
    return false;
  }
  // visualization_path
  if (!rosidl_runtime_c__String__copy(
      &(input->visualization_path), &(output->visualization_path)))
  {
    return false;
  }
  return true;
}

insp_interfaces__srv__RecognizeInspection_Response *
insp_interfaces__srv__RecognizeInspection_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__RecognizeInspection_Response * msg = (insp_interfaces__srv__RecognizeInspection_Response *)allocator.allocate(sizeof(insp_interfaces__srv__RecognizeInspection_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(insp_interfaces__srv__RecognizeInspection_Response));
  bool success = insp_interfaces__srv__RecognizeInspection_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
insp_interfaces__srv__RecognizeInspection_Response__destroy(insp_interfaces__srv__RecognizeInspection_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    insp_interfaces__srv__RecognizeInspection_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
insp_interfaces__srv__RecognizeInspection_Response__Sequence__init(insp_interfaces__srv__RecognizeInspection_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__RecognizeInspection_Response * data = NULL;

  if (size) {
    data = (insp_interfaces__srv__RecognizeInspection_Response *)allocator.zero_allocate(size, sizeof(insp_interfaces__srv__RecognizeInspection_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = insp_interfaces__srv__RecognizeInspection_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        insp_interfaces__srv__RecognizeInspection_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
insp_interfaces__srv__RecognizeInspection_Response__Sequence__fini(insp_interfaces__srv__RecognizeInspection_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      insp_interfaces__srv__RecognizeInspection_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

insp_interfaces__srv__RecognizeInspection_Response__Sequence *
insp_interfaces__srv__RecognizeInspection_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__RecognizeInspection_Response__Sequence * array = (insp_interfaces__srv__RecognizeInspection_Response__Sequence *)allocator.allocate(sizeof(insp_interfaces__srv__RecognizeInspection_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = insp_interfaces__srv__RecognizeInspection_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
insp_interfaces__srv__RecognizeInspection_Response__Sequence__destroy(insp_interfaces__srv__RecognizeInspection_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    insp_interfaces__srv__RecognizeInspection_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
insp_interfaces__srv__RecognizeInspection_Response__Sequence__are_equal(const insp_interfaces__srv__RecognizeInspection_Response__Sequence * lhs, const insp_interfaces__srv__RecognizeInspection_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!insp_interfaces__srv__RecognizeInspection_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
insp_interfaces__srv__RecognizeInspection_Response__Sequence__copy(
  const insp_interfaces__srv__RecognizeInspection_Response__Sequence * input,
  insp_interfaces__srv__RecognizeInspection_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(insp_interfaces__srv__RecognizeInspection_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    insp_interfaces__srv__RecognizeInspection_Response * data =
      (insp_interfaces__srv__RecognizeInspection_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!insp_interfaces__srv__RecognizeInspection_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          insp_interfaces__srv__RecognizeInspection_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!insp_interfaces__srv__RecognizeInspection_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
