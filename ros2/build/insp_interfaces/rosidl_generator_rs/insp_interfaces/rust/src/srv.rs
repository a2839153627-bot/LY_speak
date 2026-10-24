#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to insp_interfaces__srv__RecognizeInspection_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RecognizeInspection_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub algorithm: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub image_path: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub output_dir: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub resource_dir: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub task_dir: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub point_id: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub point_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub node_type: std::string::String,

}



impl Default for RecognizeInspection_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::RecognizeInspection_Request::default())
  }
}

impl rosidl_runtime_rs::Message for RecognizeInspection_Request {
  type RmwMsg = super::srv::rmw::RecognizeInspection_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        algorithm: msg.algorithm.as_str().into(),
        image_path: msg.image_path.as_str().into(),
        output_dir: msg.output_dir.as_str().into(),
        resource_dir: msg.resource_dir.as_str().into(),
        task_dir: msg.task_dir.as_str().into(),
        point_id: msg.point_id,
        point_name: msg.point_name.as_str().into(),
        node_type: msg.node_type.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        algorithm: msg.algorithm.as_str().into(),
        image_path: msg.image_path.as_str().into(),
        output_dir: msg.output_dir.as_str().into(),
        resource_dir: msg.resource_dir.as_str().into(),
        task_dir: msg.task_dir.as_str().into(),
      point_id: msg.point_id,
        point_name: msg.point_name.as_str().into(),
        node_type: msg.node_type.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      algorithm: msg.algorithm.to_string(),
      image_path: msg.image_path.to_string(),
      output_dir: msg.output_dir.to_string(),
      resource_dir: msg.resource_dir.to_string(),
      task_dir: msg.task_dir.to_string(),
      point_id: msg.point_id,
      point_name: msg.point_name.to_string(),
      node_type: msg.node_type.to_string(),
    }
  }
}


// Corresponds to insp_interfaces__srv__RecognizeInspection_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RecognizeInspection_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result_json: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub visualization_path: std::string::String,

}



impl Default for RecognizeInspection_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::RecognizeInspection_Response::default())
  }
}

impl rosidl_runtime_rs::Message for RecognizeInspection_Response {
  type RmwMsg = super::srv::rmw::RecognizeInspection_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        result_json: msg.result_json.as_str().into(),
        visualization_path: msg.visualization_path.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
        result_json: msg.result_json.as_str().into(),
        visualization_path: msg.visualization_path.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      result_json: msg.result_json.to_string(),
      visualization_path: msg.visualization_path.to_string(),
    }
  }
}


// Corresponds to insp_interfaces__srv__Speak_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Speak_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub text: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub interrupt_current: bool,

}



impl Default for Speak_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Speak_Request::default())
  }
}

impl rosidl_runtime_rs::Message for Speak_Request {
  type RmwMsg = super::srv::rmw::Speak_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        text: msg.text.as_str().into(),
        interrupt_current: msg.interrupt_current,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        text: msg.text.as_str().into(),
      interrupt_current: msg.interrupt_current,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      text: msg.text.to_string(),
      interrupt_current: msg.interrupt_current,
    }
  }
}


// Corresponds to insp_interfaces__srv__Speak_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Speak_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for Speak_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::Speak_Response::default())
  }
}

impl rosidl_runtime_rs::Message for Speak_Response {
  type RmwMsg = super::srv::rmw::Speak_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        accepted: msg.accepted,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      accepted: msg.accepted,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      accepted: msg.accepted,
      message: msg.message.to_string(),
    }
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


