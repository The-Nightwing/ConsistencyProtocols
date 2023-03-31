from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class DeleteRequestServer(_message.Message):
    __slots__ = ["timestamp", "uuid"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    uuid: str
    def __init__(self, uuid: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class ReadRequest(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class ReadResponse(_message.Message):
    __slots__ = ["content", "name", "status", "timestamp"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    content: str
    name: str
    status: str
    timestamp: str
    def __init__(self, status: _Optional[str] = ..., name: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class WriteRequest(_message.Message):
    __slots__ = ["content", "name", "uuid"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    content: str
    name: str
    uuid: str
    def __init__(self, name: _Optional[str] = ..., content: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class WriteRequestServer(_message.Message):
    __slots__ = ["content", "name", "timestamp", "uuid"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    content: str
    name: str
    timestamp: str
    uuid: str
    def __init__(self, name: _Optional[str] = ..., content: _Optional[str] = ..., uuid: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class WriteResponse(_message.Message):
    __slots__ = ["status", "timestamp", "uuid"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    status: str
    timestamp: str
    uuid: str
    def __init__(self, status: _Optional[str] = ..., uuid: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class serverData(_message.Message):
    __slots__ = ["name", "port"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    port: str
    def __init__(self, name: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class serverDataResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
