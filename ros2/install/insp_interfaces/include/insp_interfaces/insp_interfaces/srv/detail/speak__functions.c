// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from insp_interfaces:srv/Speak.idl
// generated code does not contain a copyright notice
#include "insp_interfaces/srv/detail/speak__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `text`
#include "rosidl_runtime_c/string_functions.h"

bool
insp_interfaces__srv__Speak_Request__init(insp_interfaces__srv__Speak_Request * msg)
{
  if (!msg) {
    return false;
  }
  // text
  if (!rosidl_runtime_c__String__init(&msg->text)) {
    insp_interfaces__srv__Speak_Request__fini(msg);
    return false;
  }
  // interrupt_current
  return true;
}

void
insp_interfaces__srv__Speak_Request__fini(insp_interfaces__srv__Speak_Request * msg)
{
  if (!msg) {
    return;
  }
  // text
  rosidl_runtime_c__String__fini(&msg->text);
  // interrupt_current
}

bool
insp_interfaces__srv__Speak_Request__are_equal(const insp_interfaces__srv__Speak_Request * lhs, const insp_interfaces__srv__Speak_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // text
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->text), &(rhs->text)))
  {
    return false;
  }
  // interrupt_current
  if (lhs->interrupt_current != rhs->interrupt_current) {
    return false;
  }
  return true;
}

bool
insp_interfaces__srv__Speak_Request__copy(
  const insp_interfaces__srv__Speak_Request * input,
  insp_interfaces__srv__Speak_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // text
  if (!rosidl_runtime_c__String__copy(
      &(input->text), &(output->text)))
  {
    return false;
  }
  // interrupt_current
  output->interrupt_current = input->interrupt_current;
  return true;
}

insp_interfaces__srv__Speak_Request *
insp_interfaces__srv__Speak_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__Speak_Request * msg = (insp_interfaces__srv__Speak_Request *)allocator.allocate(sizeof(insp_interfaces__srv__Speak_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(insp_interfaces__srv__Speak_Request));
  bool success = insp_interfaces__srv__Speak_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
insp_interfaces__srv__Speak_Request__destroy(insp_interfaces__srv__Speak_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    insp_interfaces__srv__Speak_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
insp_interfaces__srv__Speak_Request__Sequence__init(insp_interfaces__srv__Speak_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__Speak_Request * data = NULL;

  if (size) {
    data = (insp_interfaces__srv__Speak_Request *)allocator.zero_allocate(size, sizeof(insp_interfaces__srv__Speak_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = insp_interfaces__srv__Speak_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        insp_interfaces__srv__Speak_Request__fini(&data[i - 1]);
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
insp_interfaces__srv__Speak_Request__Sequence__fini(insp_interfaces__srv__Speak_Request__Sequence * array)
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
      insp_interfaces__srv__Speak_Request__fini(&array->data[i]);
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

insp_interfaces__srv__Speak_Request__Sequence *
insp_interfaces__srv__Speak_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__Speak_Request__Sequence * array = (insp_interfaces__srv__Speak_Request__Sequence *)allocator.allocate(sizeof(insp_interfaces__srv__Speak_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = insp_interfaces__srv__Speak_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
insp_interfaces__srv__Speak_Request__Sequence__destroy(insp_interfaces__srv__Speak_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    insp_interfaces__srv__Speak_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
insp_interfaces__srv__Speak_Request__Sequence__are_equal(const insp_interfaces__srv__Speak_Request__Sequence * lhs, const insp_interfaces__srv__Speak_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!insp_interfaces__srv__Speak_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
insp_interfaces__srv__Speak_Request__Sequence__copy(
  const insp_interfaces__srv__Speak_Request__Sequence * input,
  insp_interfaces__srv__Speak_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(insp_interfaces__srv__Speak_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    insp_interfaces__srv__Speak_Request * data =
      (insp_interfaces__srv__Speak_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!insp_interfaces__srv__Speak_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          insp_interfaces__srv__Speak_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!insp_interfaces__srv__Speak_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
insp_interfaces__srv__Speak_Response__init(insp_interfaces__srv__Speak_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    insp_interfaces__srv__Speak_Response__fini(msg);
    return false;
  }
  return true;
}

void
insp_interfaces__srv__Speak_Response__fini(insp_interfaces__srv__Speak_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
insp_interfaces__srv__Speak_Response__are_equal(const insp_interfaces__srv__Speak_Response * lhs, const insp_interfaces__srv__Speak_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
insp_interfaces__srv__Speak_Response__copy(
  const insp_interfaces__srv__Speak_Response * input,
  insp_interfaces__srv__Speak_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

insp_interfaces__srv__Speak_Response *
insp_interfaces__srv__Speak_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__Speak_Response * msg = (insp_interfaces__srv__Speak_Response *)allocator.allocate(sizeof(insp_interfaces__srv__Speak_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(insp_interfaces__srv__Speak_Response));
  bool success = insp_interfaces__srv__Speak_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
insp_interfaces__srv__Speak_Response__destroy(insp_interfaces__srv__Speak_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    insp_interfaces__srv__Speak_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
insp_interfaces__srv__Speak_Response__Sequence__init(insp_interfaces__srv__Speak_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__Speak_Response * data = NULL;

  if (size) {
    data = (insp_interfaces__srv__Speak_Response *)allocator.zero_allocate(size, sizeof(insp_interfaces__srv__Speak_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = insp_interfaces__srv__Speak_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        insp_interfaces__srv__Speak_Response__fini(&data[i - 1]);
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
insp_interfaces__srv__Speak_Response__Sequence__fini(insp_interfaces__srv__Speak_Response__Sequence * array)
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
      insp_interfaces__srv__Speak_Response__fini(&array->data[i]);
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

insp_interfaces__srv__Speak_Response__Sequence *
insp_interfaces__srv__Speak_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  insp_interfaces__srv__Speak_Response__Sequence * array = (insp_interfaces__srv__Speak_Response__Sequence *)allocator.allocate(sizeof(insp_interfaces__srv__Speak_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = insp_interfaces__srv__Speak_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
insp_interfaces__srv__Speak_Response__Sequence__destroy(insp_interfaces__srv__Speak_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    insp_interfaces__srv__Speak_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
insp_interfaces__srv__Speak_Response__Sequence__are_equal(const insp_interfaces__srv__Speak_Response__Sequence * lhs, const insp_interfaces__srv__Speak_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!insp_interfaces__srv__Speak_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
insp_interfaces__srv__Speak_Response__Sequence__copy(
  const insp_interfaces__srv__Speak_Response__Sequence * input,
  insp_interfaces__srv__Speak_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(insp_interfaces__srv__Speak_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    insp_interfaces__srv__Speak_Response * data =
      (insp_interfaces__srv__Speak_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!insp_interfaces__srv__Speak_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          insp_interfaces__srv__Speak_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!insp_interfaces__srv__Speak_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
