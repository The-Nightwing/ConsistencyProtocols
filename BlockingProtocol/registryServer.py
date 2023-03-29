import grpc
import registryServer_pb2
import registryServer_pb2_grpc

from concurrent import futures

class RegistryServer(registryServer_pb2_grpc.RegistryServerServicer):
    def __init__(self) -> None:
        super().__init__()
        self.replicaList = []
        self.nonPrimaryServers = []
        self.primaryServer = {}
    
    def Register(self, request, context):
        print('JOIN REQUEST FROM localhost:', request.address)
        if len(self.replicaList) == 0:
            self.primaryServer = {
                'host': 'localhost',
                'port': request.address
            }
        self.replicaList.append(request)

        if request.address!=self.primaryServer['port']:
            self.nonPrimaryServers.append(request)

        return registryServer_pb2.Response(host = 'localhost', port = self.primaryServer['port'])
    
    def GetServerList(self, request, context):
        print('SERVER LIST REQUEST FROM CLIENT')
        responseServerList = []
        for server in self.replicaList:
            responseServerList.append(registryServer_pb2.serverListResponse.ServerDetails(host = 'localhost', port = server.address))

        return registryServer_pb2.serverListResponse(serverDetails = responseServerList)
    

if __name__=='__main__':
    port = '8888'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registryServer_pb2_grpc.add_RegistryServerServicer_to_server(RegistryServer(),server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()