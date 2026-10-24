#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "insp_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__RecognizeInspection_Request() -> *const std::ffi::c_void;
}

#[link(name = "insp_interfaces__rosidl_generator_c")]
extern "C" {
    fn insp_interfaces__srv__RecognizeInspection_Request__init(msg: *mut RecognizeInspection_Request) -> bool;
    fn insp_interfaces__srv__RecognizeInspection_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RecognizeInspection_Request>, size: usize) -> bool;
    fn insp_interfaces__srv__RecognizeInspection_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RecognizeInspection_Request>);
    fn insp_interfaces__srv__RecognizeInspection_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RecognizeInspection_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<RecognizeInspection_Request>) -> bool;
}

// Corresponds to insp_interfaces__srv__RecognizeInspection_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RecognizeInspection_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub algorithm: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image_path: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub output_dir: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub resource_dir: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub task_dir: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub point_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub point_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub node_type: rosidl_runtime_rs::String,

}



impl Default for RecognizeInspection_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !insp_interfaces__srv__RecognizeInspection_Request__init(&mut msg as *mut _) {
        panic!("Call to insp_interfaces__srv__RecognizeInspection_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RecognizeInspection_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__RecognizeInspection_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__RecognizeInspection_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__RecognizeInspection_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RecognizeInspection_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RecognizeInspection_Request where Self: Sized {
  const TYPE_NAME: &'static str = "insp_interfaces/srv/RecognizeInspection_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__RecognizeInspection_Request() }
  }
}


#[link(name = "insp_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__RecognizeInspection_Response() -> *const std::ffi::c_void;
}

#[link(name = "insp_interfaces__rosidl_generator_c")]
extern "C" {
    fn insp_interfaces__srv__RecognizeInspection_Response__init(msg: *mut RecognizeInspection_Response) -> bool;
    fn insp_interfaces__srv__RecognizeInspection_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RecognizeInspection_Response>, size: usize) -> bool;
    fn insp_interfaces__srv__RecognizeInspection_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RecognizeInspection_Response>);
    fn insp_interfaces__srv__RecognizeInspection_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RecognizeInspection_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<RecognizeInspection_Response>) -> bool;
}

// Corresponds to insp_interfaces__srv__RecognizeInspection_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RecognizeInspection_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result_json: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub visualization_path: rosidl_runtime_rs::String,

}



impl Default for RecognizeInspection_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !insp_interfaces__srv__RecognizeInspection_Response__init(&mut msg as *mut _) {
        panic!("Call to insp_interfaces__srv__RecognizeInspection_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RecognizeInspection_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__RecognizeInspection_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__RecognizeInspection_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__RecognizeInspection_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RecognizeInspection_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RecognizeInspection_Response where Self: Sized {
  const TYPE_NAME: &'static str = "insp_interfaces/srv/RecognizeInspection_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__RecognizeInspection_Response() }
  }
}


#[link(name = "insp_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__Speak_Request() -> *const std::ffi::c_void;
}

#[link(name = "insp_interfaces__rosidl_generator_c")]
extern "C" {
    fn insp_interfaces__srv__Speak_Request__init(msg: *mut Speak_Request) -> bool;
    fn insp_interfaces__srv__Speak_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Speak_Request>, size: usize) -> bool;
    fn insp_interfaces__srv__Speak_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Speak_Request>);
    fn insp_interfaces__srv__Speak_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Speak_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<Speak_Request>) -> bool;
}

// Corresponds to insp_interfaces__srv__Speak_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Speak_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub text: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub interrupt_current: bool,

}



impl Default for Speak_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !insp_interfaces__srv__Speak_Request__init(&mut msg as *mut _) {
        panic!("Call to insp_interfaces__srv__Speak_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Speak_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__Speak_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__Speak_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__Speak_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Speak_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Speak_Request where Self: Sized {
  const TYPE_NAME: &'static str = "insp_interfaces/srv/Speak_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__Speak_Request() }
  }
}


#[link(name = "insp_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__Speak_Response() -> *const std::ffi::c_void;
}

#[link(name = "insp_interfaces__rosidl_generator_c")]
extern "C" {
    fn insp_interfaces__srv__Speak_Response__init(msg: *mut Speak_Response) -> bool;
    fn insp_interfaces__srv__Speak_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Speak_Response>, size: usize) -> bool;
    fn insp_interfaces__srv__Speak_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Speak_Response>);
    fn insp_interfaces__srv__Speak_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Speak_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<Speak_Response>) -> bool;
}

// Corresponds to insp_interfaces__srv__Speak_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Speak_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for Speak_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !insp_interfaces__srv__Speak_Response__init(&mut msg as *mut _) {
        panic!("Call to insp_interfaces__srv__Speak_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Speak_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__Speak_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__Speak_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { insp_interfaces__srv__Speak_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Speak_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Speak_Response where Self: Sized {
  const TYPE_NAME: &'static str = "insp_interfaces/srv/Speak_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__insp_interfaces__srv__Speak_Response() }
  }
}






#[link(name = "insp_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__insp_interfaces__srv__RecognizeInspection() -> *const std::ffi::c_void;
}

// Corresponds to insp_interfaces__srv__RecognizeInspection
#[allow(missing_docs, non_camel_case_types)]
pub struct RecognizeInspection;

impl rosidl_runtime_rs::Service for RecognizeInspection {
    type Request = RecognizeInspection_Request;
    type Response = RecognizeInspection_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__insp_interfaces__srv__RecognizeInspection() }
    }
}




#[link(name = "insp_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__insp_interfaces__srv__Speak() -> *const std::ffi::c_void;
}

// Corresponds to insp_interfaces__srv__Speak
#[allow(missing_docs, non_camel_case_types)]
pub struct Speak;

impl rosidl_runtime_rs::Service for Speak {
    type Request = Speak_Request;
    type Response = Speak_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__insp_interfaces__srv__Speak() }
    }
}


