# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import server_pb2 as server__pb2


class ServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.read = channel.unary_unary(
                '/proto.Server/read',
                request_serializer=server__pb2.ReadRequest.SerializeToString,
                response_deserializer=server__pb2.ReadResponse.FromString,
                )
        self.writeClientRequest = channel.unary_unary(
                '/proto.Server/writeClientRequest',
                request_serializer=server__pb2.WriteRequest.SerializeToString,
                response_deserializer=server__pb2.WriteResponse.FromString,
                )
        self.writeServerRequest = channel.unary_unary(
                '/proto.Server/writeServerRequest',
                request_serializer=server__pb2.WriteRequestServer.SerializeToString,
                response_deserializer=server__pb2.WriteResponse.FromString,
                )
        self.deleteServerRequest = channel.unary_unary(
                '/proto.Server/deleteServerRequest',
                request_serializer=server__pb2.DeleteRequestServer.SerializeToString,
                response_deserializer=server__pb2.DeleteResponse.FromString,
                )
        self.deleteClientRequest = channel.unary_unary(
                '/proto.Server/deleteClientRequest',
                request_serializer=server__pb2.DeleteRequest.SerializeToString,
                response_deserializer=server__pb2.DeleteResponse.FromString,
                )
        self.addNonPrimaryServers = channel.unary_unary(
                '/proto.Server/addNonPrimaryServers',
                request_serializer=server__pb2.serverData.SerializeToString,
                response_deserializer=server__pb2.serverDataResponse.FromString,
                )


class ServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def read(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def writeClientRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def writeServerRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteServerRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteClientRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def addNonPrimaryServers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'read': grpc.unary_unary_rpc_method_handler(
                    servicer.read,
                    request_deserializer=server__pb2.ReadRequest.FromString,
                    response_serializer=server__pb2.ReadResponse.SerializeToString,
            ),
            'writeClientRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.writeClientRequest,
                    request_deserializer=server__pb2.WriteRequest.FromString,
                    response_serializer=server__pb2.WriteResponse.SerializeToString,
            ),
            'writeServerRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.writeServerRequest,
                    request_deserializer=server__pb2.WriteRequestServer.FromString,
                    response_serializer=server__pb2.WriteResponse.SerializeToString,
            ),
            'deleteServerRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteServerRequest,
                    request_deserializer=server__pb2.DeleteRequestServer.FromString,
                    response_serializer=server__pb2.DeleteResponse.SerializeToString,
            ),
            'deleteClientRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteClientRequest,
                    request_deserializer=server__pb2.DeleteRequest.FromString,
                    response_serializer=server__pb2.DeleteResponse.SerializeToString,
            ),
            'addNonPrimaryServers': grpc.unary_unary_rpc_method_handler(
                    servicer.addNonPrimaryServers,
                    request_deserializer=server__pb2.serverData.FromString,
                    response_serializer=server__pb2.serverDataResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.Server', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Server(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def read(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Server/read',
            server__pb2.ReadRequest.SerializeToString,
            server__pb2.ReadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def writeClientRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Server/writeClientRequest',
            server__pb2.WriteRequest.SerializeToString,
            server__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def writeServerRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Server/writeServerRequest',
            server__pb2.WriteRequestServer.SerializeToString,
            server__pb2.WriteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteServerRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Server/deleteServerRequest',
            server__pb2.DeleteRequestServer.SerializeToString,
            server__pb2.DeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteClientRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Server/deleteClientRequest',
            server__pb2.DeleteRequest.SerializeToString,
            server__pb2.DeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def addNonPrimaryServers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.Server/addNonPrimaryServers',
            server__pb2.serverData.SerializeToString,
            server__pb2.serverDataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
