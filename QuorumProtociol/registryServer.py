import shutil
import grpc
import registryServer_pb2
import registryServer_pb2_grpc
import server_pb2
import server_pb2_grpc
import random

from concurrent import futures

class RegistryServer(registryServer_pb2_grpc.RegistryServerServicer):
    def __init__(self, Nr, Nw, N) -> None:
        super().__init__()
        self.Nr = Nr
        self.Nw = Nw
        self.N = N
        self.replicaList = []
    
    def Register(self, request, context):
        print('JOIN REQUEST FROM localhost:', request.address)
        self.replicaList.append(request)
        return registryServer_pb2.Response(host = 'localhost', port = request.address)
    
    def GetServerList(self, request, context):
        print('SERVER LIST REQUEST FROM CLIENT')
        responseServerList = []
        for server in self.replicaList:
            responseServerList.append(registryServer_pb2.serverListResponse.ServerDetails(host = 'localhost', port = server.address))

        return registryServer_pb2.serverListResponse(serverDetails = responseServerList)
    
    def GetReadQuorum(self, request, context):
        print('READ QUORUM REQUEST FROM CLIENT')
        readList = random.sample(self.replicaList, self.Nr)
        responseServerList = []
        for server in readList:
            responseServerList.append(registryServer_pb2.serverListResponse.ServerDetails(host = 'localhost', port = server.address))
        return registryServer_pb2.serverListResponse(serverDetails=responseServerList)
    
    def GetWriteQuorum(self, request, context):
        print('WRITE QUORUM REQUEST FROM CLIENT')
        writeList = random.sample(self.replicaList, self.Nw)
        responseServerList = []
        for server in writeList:
            responseServerList.append(registryServer_pb2.serverListResponse.ServerDetails(host = 'localhost', port = server.address))
        return registryServer_pb2.serverListResponse(serverDetails=responseServerList)
    
def main():
    port = '8888'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Nr = 0
    Nw = 0
    N = 0
    while not (Nr+Nw>N and Nw*2>N):
        Nr = int(input('Nr: '))
        Nw = int(input('Nw: '))
        N = int(input('N: '))
    registryServer_pb2_grpc.add_RegistryServerServicer_to_server(RegistryServer(Nr, Nw, N),server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__=='__main__':
    main()