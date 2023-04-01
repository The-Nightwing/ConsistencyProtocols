# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import registryServer_pb2 as registryServer__pb2


class RegistryServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Register = channel.unary_unary(
                '/rpc.RegistryServer/Register',
                request_serializer=registryServer__pb2.Server.SerializeToString,
                response_deserializer=registryServer__pb2.Response.FromString,
                )
        self.GetReadQuorum = channel.unary_unary(
                '/rpc.RegistryServer/GetReadQuorum',
                request_serializer=registryServer__pb2.serverListRequest.SerializeToString,
                response_deserializer=registryServer__pb2.serverListResponse.FromString,
                )
        self.GetWriteQuorum = channel.unary_unary(
                '/rpc.RegistryServer/GetWriteQuorum',
                request_serializer=registryServer__pb2.serverListRequest.SerializeToString,
                response_deserializer=registryServer__pb2.serverListResponse.FromString,
                )
        self.GetServerList = channel.unary_unary(
                '/rpc.RegistryServer/GetServerList',
                request_serializer=registryServer__pb2.serverListRequest.SerializeToString,
                response_deserializer=registryServer__pb2.serverListResponse.FromString,
                )


class RegistryServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Register(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetReadQuorum(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWriteQuorum(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServerList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RegistryServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Register': grpc.unary_unary_rpc_method_handler(
                    servicer.Register,
                    request_deserializer=registryServer__pb2.Server.FromString,
                    response_serializer=registryServer__pb2.Response.SerializeToString,
            ),
            'GetReadQuorum': grpc.unary_unary_rpc_method_handler(
                    servicer.GetReadQuorum,
                    request_deserializer=registryServer__pb2.serverListRequest.FromString,
                    response_serializer=registryServer__pb2.serverListResponse.SerializeToString,
            ),
            'GetWriteQuorum': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWriteQuorum,
                    request_deserializer=registryServer__pb2.serverListRequest.FromString,
                    response_serializer=registryServer__pb2.serverListResponse.SerializeToString,
            ),
            'GetServerList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerList,
                    request_deserializer=registryServer__pb2.serverListRequest.FromString,
                    response_serializer=registryServer__pb2.serverListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc.RegistryServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RegistryServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.RegistryServer/Register',
            registryServer__pb2.Server.SerializeToString,
            registryServer__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetReadQuorum(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.RegistryServer/GetReadQuorum',
            registryServer__pb2.serverListRequest.SerializeToString,
            registryServer__pb2.serverListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetWriteQuorum(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.RegistryServer/GetWriteQuorum',
            registryServer__pb2.serverListRequest.SerializeToString,
            registryServer__pb2.serverListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServerList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.RegistryServer/GetServerList',
            registryServer__pb2.serverListRequest.SerializeToString,
            registryServer__pb2.serverListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
