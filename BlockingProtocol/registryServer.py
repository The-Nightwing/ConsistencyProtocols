import shutil
import grpc
import registryServer_pb2
import registryServer_pb2_grpc
import server_pb2
import server_pb2_grpc

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
            with grpc.insecure_channel('localhost:' + self.primaryServer['port']) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                stub.addNonPrimaryServers(server_pb2.serverData(name = request.name, port = request.address))

        return registryServer_pb2.Response(host = 'localhost', port = self.primaryServer['port'])
    
    def GetServerList(self, request, context):
        print('SERVER LIST REQUEST FROM CLIENT')
        responseServerList = []
        for server in self.replicaList:
            responseServerList.append(registryServer_pb2.serverListResponse.ServerDetails(host = 'localhost', port = server.address))

        return registryServer_pb2.serverListResponse(serverDetails = responseServerList)
    
def main():
    port = '8888'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registryServer_pb2_grpc.add_RegistryServerServicer_to_server(RegistryServer(),server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__=='__main__':
    main()