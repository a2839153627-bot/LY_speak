# generated from rosidl_generator_py/resource/_idl.py.em
# with input from insp_interfaces:srv/RecognizeInspection.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_RecognizeInspection_Request(type):
    """Metaclass of message 'RecognizeInspection_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('insp_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'insp_interfaces.srv.RecognizeInspection_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__recognize_inspection__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__recognize_inspection__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__recognize_inspection__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__recognize_inspection__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__recognize_inspection__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RecognizeInspection_Request(metaclass=Metaclass_RecognizeInspection_Request):
    """Message class 'RecognizeInspection_Request'."""

    __slots__ = [
        '_algorithm',
        '_image_path',
        '_output_dir',
        '_resource_dir',
        '_task_dir',
        '_point_id',
        '_point_name',
        '_node_type',
    ]

    _fields_and_field_types = {
        'algorithm': 'string',
        'image_path': 'string',
        'output_dir': 'string',
        'resource_dir': 'string',
        'task_dir': 'string',
        'point_id': 'int32',
        'point_name': 'string',
        'node_type': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('int32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.algorithm = kwargs.get('algorithm', str())
        self.image_path = kwargs.get('image_path', str())
        self.output_dir = kwargs.get('output_dir', str())
        self.resource_dir = kwargs.get('resource_dir', str())
        self.task_dir = kwargs.get('task_dir', str())
        self.point_id = kwargs.get('point_id', int())
        self.point_name = kwargs.get('point_name', str())
        self.node_type = kwargs.get('node_type', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.algorithm != other.algorithm:
            return False
        if self.image_path != other.image_path:
            return False
        if self.output_dir != other.output_dir:
            return False
        if self.resource_dir != other.resource_dir:
            return False
        if self.task_dir != other.task_dir:
            return False
        if self.point_id != other.point_id:
            return False
        if self.point_name != other.point_name:
            return False
        if self.node_type != other.node_type:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def algorithm(self):
        """Message field 'algorithm'."""
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'algorithm' field must be of type 'str'"
        self._algorithm = value

    @builtins.property
    def image_path(self):
        """Message field 'image_path'."""
        return self._image_path

    @image_path.setter
    def image_path(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'image_path' field must be of type 'str'"
        self._image_path = value

    @builtins.property
    def output_dir(self):
        """Message field 'output_dir'."""
        return self._output_dir

    @output_dir.setter
    def output_dir(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'output_dir' field must be of type 'str'"
        self._output_dir = value

    @builtins.property
    def resource_dir(self):
        """Message field 'resource_dir'."""
        return self._resource_dir

    @resource_dir.setter
    def resource_dir(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'resource_dir' field must be of type 'str'"
        self._resource_dir = value

    @builtins.property
    def task_dir(self):
        """Message field 'task_dir'."""
        return self._task_dir

    @task_dir.setter
    def task_dir(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'task_dir' field must be of type 'str'"
        self._task_dir = value

    @builtins.property
    def point_id(self):
        """Message field 'point_id'."""
        return self._point_id

    @point_id.setter
    def point_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'point_id' field must be of type 'int'"
            assert value >= -2147483648 and value < 2147483648, \
                "The 'point_id' field must be an integer in [-2147483648, 2147483647]"
        self._point_id = value

    @builtins.property
    def point_name(self):
        """Message field 'point_name'."""
        return self._point_name

    @point_name.setter
    def point_name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'point_name' field must be of type 'str'"
        self._point_name = value

    @builtins.property
    def node_type(self):
        """Message field 'node_type'."""
        return self._node_type

    @node_type.setter
    def node_type(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'node_type' field must be of type 'str'"
        self._node_type = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_RecognizeInspection_Response(type):
    """Metaclass of message 'RecognizeInspection_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('insp_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'insp_interfaces.srv.RecognizeInspection_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__recognize_inspection__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__recognize_inspection__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__recognize_inspection__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__recognize_inspection__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__recognize_inspection__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class RecognizeInspection_Response(metaclass=Metaclass_RecognizeInspection_Response):
    """Message class 'RecognizeInspection_Response'."""

    __slots__ = [
        '_success',
        '_message',
        '_result_json',
        '_visualization_path',
    ]

    _fields_and_field_types = {
        'success': 'boolean',
        'message': 'string',
        'result_json': 'string',
        'visualization_path': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.success = kwargs.get('success', bool())
        self.message = kwargs.get('message', str())
        self.result_json = kwargs.get('result_json', str())
        self.visualization_path = kwargs.get('visualization_path', str())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.success != other.success:
            return False
        if self.message != other.message:
            return False
        if self.result_json != other.result_json:
            return False
        if self.visualization_path != other.visualization_path:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def success(self):
        """Message field 'success'."""
        return self._success

    @success.setter
    def success(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'success' field must be of type 'bool'"
        self._success = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value

    @builtins.property
    def result_json(self):
        """Message field 'result_json'."""
        return self._result_json

    @result_json.setter
    def result_json(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'result_json' field must be of type 'str'"
        self._result_json = value

    @builtins.property
    def visualization_path(self):
        """Message field 'visualization_path'."""
        return self._visualization_path

    @visualization_path.setter
    def visualization_path(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'visualization_path' field must be of type 'str'"
        self._visualization_path = value


class Metaclass_RecognizeInspection(type):
    """Metaclass of service 'RecognizeInspection'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('insp_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'insp_interfaces.srv.RecognizeInspection')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__recognize_inspection

            from insp_interfaces.srv import _recognize_inspection
            if _recognize_inspection.Metaclass_RecognizeInspection_Request._TYPE_SUPPORT is None:
                _recognize_inspection.Metaclass_RecognizeInspection_Request.__import_type_support__()
            if _recognize_inspection.Metaclass_RecognizeInspection_Response._TYPE_SUPPORT is None:
                _recognize_inspection.Metaclass_RecognizeInspection_Response.__import_type_support__()


class RecognizeInspection(metaclass=Metaclass_RecognizeInspection):
    from insp_interfaces.srv._recognize_inspection import RecognizeInspection_Request as Request
    from insp_interfaces.srv._recognize_inspection import RecognizeInspection_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
