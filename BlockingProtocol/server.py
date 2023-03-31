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

        if isPrimary:
            self.nonPrimaryServers = []
    
    
    def read(self, request, context):
        if request.uuid not in self.fileObject:
            return server_pb2.ReadResponse(status = 'FAIL')
        
        if request.uuid in self.fileObject:
            if os.path.exists('files/'+self.name+'/'+self.fileObject[request.uuid]['filename']):
                with open('files/'+self.name+'/'+self.fileObject[request.uuid]['filename'], 'r') as f:
                    content = f.read()
                # content = self.fileObject[request.uuid]['content']
                return server_pb2.ReadResponse(status = 'SUCCESS', content = content, name = self.fileObject[request.uuid]['filename'], timestamp = self.fileObject[request.uuid]['timestamp'])
            else:
                return server_pb2.ReadResponse(status = 'FILE ALREADY DELETED', name=None, timestamp=self.fileObject[request.uuid]['timestamp'])
    
    def addNonPrimaryServers(self, request, context):
        self.nonPrimaryServers.append(request.port)
        return server_pb2.serverDataResponse(status = 'SUCCESS')


    def writeOnNonPrimaryServers(self, request, port, timestamp):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.writeServerRequest(server_pb2.WriteRequestServer(name = request.name, content = request.content, uuid = request.uuid, timestamp = timestamp))
            if response.status!='SUCCESS':
                return server_pb2.WriteResponse(status = 'FAIL')
                
    def writeServerRequest(self, request, context):
        if request.uuid not in self.fileObject:
            if os.path.exists('files/'+self.name+'/'+request.name):
                return server_pb2.WriteResponse(status = 'FILE WITH THE SAME NAME ALREADY EXISTS')
            else:
               
                if self.isPrimary:
                    # write contents in filename using write 
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    timestamp = str(time.now())
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': timestamp
                    }

                    for server in self.nonPrimaryServers:
                        # thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server, timestamp))
                        # thread.start()
                        self.writeOnNonPrimaryServers(request, server, timestamp)

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp = timestamp)
                    
                else:
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)

                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': request.timestamp
                    }

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp = request.timestamp)
        else:
            
            if os.path.exists('files/'+self.name+'/'+request.name):

                if self.isPrimary:
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    timestamp = str(time.now())
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': timestamp
                    }

                    for server in self.nonPrimaryServers:
                        # thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server, timestamp))
                        # thread.start()
                        self.writeOnNonPrimaryServers(request, server, timestamp)

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp = timestamp)

                else:
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)

                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': request.timestamp
                    }

                    return server_pb2.WriteResponse(status = 'SUCCESS',uuid=request.uuid, timestamp = request.timestamp)
            else:
                return server_pb2.WriteResponse(status = 'DELETED FILE CANNOT BE UPDATED')
            

    def writeClientRequest(self, request, context):
        if request.uuid not in self.fileObject:
            if os.path.exists('files/'+self.name+'/'+request.name):
                return server_pb2.WriteResponse(status = 'FILE WITH THE SAME NAME ALREADY EXISTS')
            else:
                if self.isPrimary:
                    # write contents in filename using write
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    timestamp = str(time.now())
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': timestamp,
                    }

                    for server in self.nonPrimaryServers:
                        self.writeOnNonPrimaryServers(request, server, timestamp)
                        # thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server, timestamp))
                        # thread.start()

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp = timestamp)
                
                else:
                    with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                        stub = server_pb2_grpc.ServerStub(channel)
                        response = stub.writeServerRequest(server_pb2.WriteRequestServer(name=request.name, content=request.content, uuid=request.uuid, timestamp = str(time.now())))
                        if response.status!='SUCCESS':
                            return server_pb2.WriteResponse(status = 'FAIL')
                        
                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp = response.timestamp)
        else:
            if os.path.exists('files/'+self.name+'/'+request.name):

                if self.isPrimary:
                    # write contents in filename using write
                    with open('files/'+self.name+'/'+request.name, 'w') as f:
                        f.write(request.content)
                    
                    timestamp = str(time.now())
                    self.fileObject[request.uuid] = {
                        'filename': request.name,
                        'timestamp': timestamp
                    }

                    for server in self.nonPrimaryServers:
                        self.writeOnNonPrimaryServers(request, server, timestamp)
                        # thread = threading.Thread(target=self.writeOnNonPrimaryServers, args=(request, server, timestamp))
                        # thread.start()

                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp=timestamp)
                
                else:
                    with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                        stub = server_pb2_grpc.ServerStub(channel)
                        response = stub.writeServerRequest(server_pb2.WriteRequestServer(name=request.name, content=request.content, uuid=request.uuid, timestamp = str(time.now())))
                        if response.status!='SUCCESS':
                            return server_pb2.WriteResponse(status = 'FAIL')
                    return server_pb2.WriteResponse(status = 'SUCCESS', uuid=request.uuid, timestamp = response.timestamp)
            else:
                return server_pb2.WriteResponse(status = 'DELETED FILE CANNOT BE UPDATED')
        
    def deleteOnNonPrimaryServers(self, request, server, timestamp):
        with grpc.insecure_channel('localhost:'+server) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.deleteServerRequest(server_pb2.DeleteRequestServer(uuid=request.uuid, timestamp = timestamp))
            if response.status!='SUCCESS':
                return server_pb2.DeleteResponse(status = 'FAIL')
    
    def deleteClientRequest(self, request, context):
        if request.uuid not in self.fileObject:
            return server_pb2.DeleteResponse(status = 'FILE DOES NOT EXIST')
        else:
            if self.fileObject[request.uuid]['filename']!='':
                if os.path.exists('files/'+self.name+'/'+self.fileObject[request.uuid]['filename']):
                    if self.isPrimary:
                        
                        os.remove('files/'+self.name+'/'+self.fileObject[request.uuid]['filename'])
                        timestamp = str(time.now())
                        self.fileObject[request.uuid]['filename'] = ''
                        self.fileObject[request.uuid]['timestamp'] = timestamp

                        for server in self.nonPrimaryServers:
                            self.deleteOnNonPrimaryServers(request, server, timestamp)
                            # thread = threading.Thread(target=self.deleteOnNonPrimaryServers, args=(request, server, timestamp))
                            # thread.start()

                        return server_pb2.DeleteResponse(status = 'SUCCESS')
                    else:
                        with grpc.insecure_channel('localhost:'+self.primaryServer['port']) as channel:
                            stub = server_pb2_grpc.ServerStub(channel)
                            response = stub.deleteServerRequest(server_pb2.DeleteRequestServer(uuid=request.uuid, timestamp = str(time.now())))
                            if response.status!='SUCCESS':
                                return server_pb2.Response(status = 'FAIL')
                        return server_pb2.DeleteResponse(status = 'SUCCESS')
            else:
                return server_pb2.DeleteResponse(status = 'FILE ALREADY DELETED')

    def deleteServerRequest(self, request, context):
        if request.uuid not in self.fileObject:
            return server_pb2.DeleteResponse(status = 'FILE DOES NOT EXIST')
        else:
            if self.fileObject[request.uuid]['filename']!='':
                if os.path.exists('files/'+self.name+'/'+self.fileObject[request.uuid]['filename']):
                    if self.isPrimary:
                        #delete this file
                        os.remove('files/'+self.name+'/'+self.fileObject[request.uuid]['filename'])
                        timestamp = str(time.now())
                        self.fileObject[request.uuid]['filename'] = ''
                        self.fileObject[request.uuid]['timestamp'] = timestamp

                        for server in self.nonPrimaryServers:
                            self.deleteOnNonPrimaryServers(request, server, timestamp)
                            # thread = threading.Thread(target=self.deleteOnNonPrimaryServers, args=(request, server, timestamp))
                            # thread.start()

                        return server_pb2.DeleteResponse(status = 'SUCCESS')
                    else:
                        os.remove('files/'+self.name+'/'+self.fileObject[request.uuid]['filename'])
                        self.fileObject[request.uuid]['filename'] = ''
                        self.fileObject[request.uuid]['timestamp'] = request.timestamp

                        return server_pb2.DeleteResponse(status = 'SUCCESS')
            else:
                return server_pb2.DeleteResponse(status = 'FILE ALREADY DELETED')


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