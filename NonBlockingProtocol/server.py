import grpc
import server_pb2
import server_pb2_grpc
import registryServer_pb2
import registryServer_pb2_grpc
import time as ti
import os
from datetime import datetime as time
from concurrent import futures
import threading


class Server(server_pb2_grpc.ServerServicer):
    def __init__(self, name, port, isPrimary) -> None:
        super().__init__()
        self.fileObject = dict()
        self.isPrimary = isPrimary
        self.name = name
        os.mkdir('files/'+self.name)
        self.primaryServer = {
            'host': 'localhost',
            'port': port
        }
        self.nonPrimaryServers = []
    
    
    def read(self, request, context):
        if request.uuid not in self.fileObject:
            return server_pb2.ReadResponse(status = 'FAIL')
        
        if request.uuid in self.fileObject:
            if os.path.exists(self.name+'/'+self.fileObject[request.uuid]['filename']):
                return server_pb2.ReadResponse(status = 'SUCCESS', filename = self.fileObject[request.uuid]['filename'], timestamp = self.fileObject[request.uuid]['timestamp'])
            else:
                return server_pb2.ReadResponse(status = 'FILE ALREADY DELETED', filename=None, timestamp=self.fileObject[request.uuid]['timestamp'])
            
    def getNonPrimaryServers(self):
        self.nonPrimaryServers = []
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = registryServer_pb2_grpc.RegistryServerStub(channel)
            response = stub.GetServerList(registryServer_pb2.serverListRequest())
            for server in response.serverDetails:
                if server.port!=self.primaryServer['port']:
                    self.nonPrimaryServers.append(server.port)

    def writeOnNonPrimaryServers(self, request, port):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.writeServerRequest(request)
            if response.status!='SUCCESS':
                return server_pb2.WriteResponse(status = 'FAIL')
                
    def writeServerRequest(self, request, context):
        print('writeServerRequest')
        if request.uuid not in self.fileObject:
            if os.path.exists('files/'+self.name+'/'+request.name):
                return server_pb2.WriteResponse(status = 'FILE WITH THE SAME NAME ALREADY EXISTS')
            else:
                self.getNonPrimaryServers()

                if self.isPrimary:
                    # write contents in filename using write 
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': str(time.now())
                    }

                    for server in self.nonPrimaryServers:
                        # create a thread pool and writeOnNonPrimaryServers
                        thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server))
                        thread.start()

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)
                    
                else:
                    #check if folder exists

                    # write contents in filename using write
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)

                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': str(time.now())
                    }

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)
        else:
            self.getNonPrimaryServers()
            print('heelooooo')
            print('files/'+self.name+'/'+request.name)
            if os.path.exists('files/'+self.name+'/'+request.name):

                if self.isPrimary:

                    # write contents in filename using write
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': str(time.now())
                    }

                    for server in self.nonPrimaryServers:
                        thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server))
                        thread.start()

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)

                else:
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)

                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': str(time.now())
                    }

                    return server_pb2.WriteResponse(status = 'SUCCESS',uuid=request.uuid)
            else:
                return server_pb2.WriteResponse(status = 'DELETED FILE CANNOT BE UPDATED')
            

    def writeClientRequest(self, request, context):
        if request.uuid not in self.fileObject:
            if os.path.exists('files/'+self.name+'/'+request.name):
                return server_pb2.WriteResponse(status = 'FILE WITH THE SAME NAME ALREADY EXISTS')
            else:
                self.getNonPrimaryServers()

                if self.isPrimary:

                    # write contents in filename using write
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': str(time.now())
                    }

                    for server in self.nonPrimaryServers:
                        thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server))
                        thread.start()

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)
                
                else:
                    # forward request to primary server
                    print('Not Primary')
                    with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                        stub = server_pb2_grpc.ServerStub(channel)
                        response = stub.writeServerRequest(request)
                        if response.status!='SUCCESS':
                            return server_pb2.WriteResponse(status = 'FAIL')
                        
                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)
        else:
            if os.path.exists('files/'+self.name+'/'+request.name):
                self.getNonPrimaryServers()

                if self.isPrimary:
                    # write contents in filename using write
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': str(time.now())
                    }

                    for server in self.nonPrimaryServers:
                        thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server))
                        thread.start()

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)
                
                else:
                    with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                        stub = server_pb2_grpc.ServerStub(channel)
                        response = stub.writeServerRequest(request)
                        if response.status!='SUCCESS':
                            return server_pb2.WriteResponse(status = 'FAIL')
                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid)
            else:
                return server_pb2.WriteResponse(status = 'DELETED FILE CANNOT BE UPDATED')
        
    def deleteOnNonPrimaryServers(self, request, server):
        with grpc.insecure_channel('localhost:'+server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.deleteServerRequest(request)
            if response.status!='SUCCESS':
                return server_pb2.DeleteResponse(status = 'FAIL')
    
    def deleteClientRequest(self, request, context):
        if request.uuid not in self.fileObject:
            return server_pb2.DeleteResponse(status = 'FILE DOES NOT EXIST')
        else:
            self.getNonPrimaryServers()
            if os.path.exists(self.name+'/'+self.fileObject[request.uuid]['filename']):
                if self.isPrimary:
                    #delete this file
                    os.remove(self.name+'/'+self.fileObject[request.uuid]['filename'])
                    self.fileObject[request.uuid]['filename'] = ''
                    self.fileObject[request.uuid]['timestamp'] = str(time.now())

                    for server in self.nonPrimaryServers:
                        thread = threading.Thread(target=self.deleteOnNonPrimaryServers, args=(request, server))
                        thread.start()

                    return server_pb2.DeleteResponse(status = 'SUCCESS')
                else:
                    with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                        stub = server_pb2_grpc.ServerStub(channel)
                        response = stub.deleteServerRequest(request)
                        if response.status!='SUCCESS':
                            return server_pb2.Response(status = 'FAIL')
                    return server_pb2.DeleteResponse(status = 'SUCCESS')

            else:
                return server_pb2.DeleteResponse(status = 'FILE ALREADY DELETED')

    def deleteServerRequest(self, request, context):
        if request.uuid not in self.fileObject:
            return server_pb2.DeleteResponse(status = 'FILE DOES NOT EXIST')
        else:
            self.getNonPrimaryServers()
            if os.path.exists(self.name+'/'+self.fileObject[request.uuid]['filename']):
                if self.isPrimary:
                    #delete this file
                    os.remove(self.name+'/'+self.fileObject[request.uuid]['filename'])
                    self.fileObject[request.uuid]['filename'] = ''
                    self.fileObject[request.uuid]['timestamp'] = str(time.now())

                    for server in self.nonPrimaryServers:
                        thread = threading.Thread(target=self.deleteOnNonPrimaryServers, args=(request, server))
                        thread.start()

                    return server_pb2.DeleteResponse(status = 'SUCCESS')
                else:
                    with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                        stub = server_pb2_grpc.ServerStub(channel)
                        response = stub.deleteServerRequest(request)
                        if response.status!='SUCCESS':
                            return server_pb2.DeleteResponse(status = 'FAIL')
                    return server_pb2.DeleteResponse(status = 'SUCCESS')


def serve():
    name = input('Enter server name: ')
    port = input('Enter port number: ')
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = registryServer_pb2_grpc.RegistryServerStub(channel)
        response =  stub.Register(registryServer_pb2.Server(name=name, address=port))
        if response.host and response.port:
            print('SUCCESS')
        else:
            print('FAIL')
            return
    
    isPrimary = (response.port == port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServerServicer_to_server(Server(name, response.port, isPrimary), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()
        
if __name__=='__main__':
    serve()