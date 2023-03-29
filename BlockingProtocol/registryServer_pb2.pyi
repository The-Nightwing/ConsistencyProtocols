from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Response(_message.Message):
    __slots__ = ["host", "port"]
    HOST_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    host: str
    port: str
    def __init__(self, host: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...

class Server(_message.Message):
    __slots__ = ["address", "name"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    address: str
    name: str
    def __init__(self, name: _Optional[str] = ..., address: _Optional[str] = ...) -> None: ...

class serverListRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class serverListResponse(_message.Message):
    __slots__ = ["serverDetails"]
    class ServerDetails(_message.Message):
        __slots__ = ["host", "port"]
        HOST_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        host: str
        port: str
        def __init__(self, host: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...
    SERVERDETAILS_FIELD_NUMBER: _ClassVar[int]
    serverDetails: _containers.RepeatedCompositeFieldContainer[serverListResponse.ServerDetails]
    def __init__(self, serverDetails: _Optional[_Iterable[_Union[serverListResponse.ServerDetails, _Mapping]]] = ...) -> None: ...
