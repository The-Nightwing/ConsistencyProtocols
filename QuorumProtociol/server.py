import sys
import grpc
import server_pb2
import server_pb2_grpc
import registryServer_pb2
import registryServer_pb2_grpc
import time
import os
from datetime import datetime
from concurrent import futures
import threading


class Server(server_pb2_grpc.ServerServicer):
    def __init__(self, name, port) -> None:
        super().__init__()
        self.fileObject = dict()
        self.name = name
        os.mkdir('files/'+self.name)
    
    
    def read(self, request, context):
        print('READ REQUEST for '+request.uuid)
        if request.uuid not in self.fileObject:
            return server_pb2.ReadResponse(status = 'FILE DOES NOT EXIST', name=None, content=None, timestamp=None)
        
        if request.uuid in self.fileObject:
            if self.fileObject[request.uuid]['filename']!='':
                if os.path.exists('files/'+self.name+'/'+self.fileObject[request.uuid]['filename']):
                    with open('files/'+self.name+'/'+self.fileObject[request.uuid]['filename'], 'r') as f:
                        content = f.read()
                    # content = self.fileObject[request.uuid]['content']
                    return server_pb2.ReadResponse(status = 'SUCCESS', content = content, name = self.fileObject[request.uuid]['filename'], timestamp = self.fileObject[request.uuid]['timestamp'])
            else:
                return server_pb2.ReadResponse(status = 'FILE ALREADY DELETED', name=None, timestamp=self.fileObject[request.uuid]['timestamp'])
            
            
    def write(self, request, context):
        print('WRITE REQUEST for '+request.uuid)
        if request.uuid not in self.fileObject:
            if os.path.exists('files/'+self.name+'/'+request.name):
                return server_pb2.WriteResponse(status='FILE ALREADY EXISTS', uuid=None, timestamp=None)
            else:
                with open('files/'+self.name+'/'+request.name,'w') as f:
                    f.write(request.content)
                    f.close()
                t = time.time()
                dt = datetime.fromtimestamp(t)
                self.fileObject[request.uuid] = {'filename':request.name, 'timestamp':dt.strftime("%d/%m/%Y %H:%M:%S")}
                return server_pb2.WriteResponse(status='SUCCESS', uuid=request.uuid, timestamp=self.fileObject[request.uuid]['timestamp'])
        else:
            if os.path.exists('files/'+self.name+'/'+request.name):
                with open('files/'+self.name+'/'+request.name,'w') as f:
                    f.write(request.content)
                    f.close()
                t = time.time()
                dt = datetime.fromtimestamp(t)
                self.fileObject[request.uuid] = {'filename':request.name, 'timestamp':dt.strftime("%d/%m/%Y %H:%M:%S")}
                return server_pb2.WriteResponse(status='SUCCESS', uuid=request.uuid, timestamp=self.fileObject[request.uuid]['timestamp'])
            else:
                return server_pb2.WriteResponse(status='FILE ALREADY DELETED', uuid=request.uuid, timestamp=self.fileObject[request.uuid]['timestamp'])
            
    def delete(self, request, context):
        print('DELETE REQUEST for '+request.uuid)
        if request.uuid in self.fileObject:
            if self.fileObject[request.uuid]['filename']!='' and os.path.exists('files/'+self.name+'/'+self.fileObject[request.uuid]['filename']):
                os.remove('files/'+self.name+'/'+self.fileObject[request.uuid]['filename'])
                t = time.time()
                dt = datetime.fromtimestamp(t)
                self.fileObject[request.uuid] = {'filename':'', 'timestamp':dt.strftime("%d/%m/%Y %H:%M:%S")}
                return server_pb2.DeleteResponse(status = 'SUCCESS')
            else:
                return server_pb2.DeleteResponse(status = 'FILE ALREADY DELETED')
        else:
            t = time.time()
            dt = datetime.fromtimestamp(t)
            self.fileObject[request.uuid] = {'filename':'', 'timestamp':dt.strftime("%d/%m/%Y %H:%M:%S")}
            return server_pb2.DeleteResponse(status = 'SUCCESS')


def serve(name, port):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = registryServer_pb2_grpc.RegistryServerStub(channel)
        response =  stub.Register(registryServer_pb2.Server(name=name, address=port))
        if response.host and response.port:
            print('SUCCESS')
        else:
            print('FAIL')
            return
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server_pb2_grpc.add_ServerServicer_to_server(Server(name, response.port), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

def main(name, port):
    serve(name, port)

if __name__=='__main__':
    name = sys.argv[1]
    port = sys.argv[2]
    serve(name, port)