import grpc
import server_pb2
import server_pb2_grpc
import registryServer_pb2
import registryServer_pb2_grpc
import uuid
import time
from datetime import datetime
import sys

client_name = str(uuid.uuid4())
channel = grpc.insecure_channel('localhost:50051')
stub = registryServer_pb2_grpc.RegistryServerStub(channel)
server_list = dict()
connected_server_list = dict()

class Client():
    def __init__(self, uuid):
        self.uuid = uuid

    def getServerList(self):
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = registryServer_pb2_grpc.RegistryServerStub(channel)
            response = stub.GetServerList(registryServer_pb2.serverListRequest())
            for server in response.serverDetails:
                print("Host: "+server.host+", Port: "+server.port)
                
    def getServerListInternal(self):
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = registryServer_pb2_grpc.RegistryServerStub(channel)
            return stub.GetServerList(registryServer_pb2.serverListRequest()).serverDetails
        
    def getReadQuorum(self):
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = registryServer_pb2_grpc.RegistryServerStub(channel)
            return stub.GetReadQuorum(registryServer_pb2.serverListRequest()).serverDetails
        
    def getWriteQuorum(self):
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = registryServer_pb2_grpc.RegistryServerStub(channel)
            return stub.GetWriteQuorum(registryServer_pb2.serverListRequest()).serverDetails

    def sendAllReadRequest(self,id,):
        server_list = self.getServerListInternal()
        
        latest_timestamp = 0
        dt = datetime.fromtimestamp(latest_timestamp)
        final_respone = ''
        deleted = False
        for server in server_list:
            with grpc.insecure_channel('localhost:'+server.port) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                response = stub.read(server_pb2.ReadRequest(uuid=id))
                print('RESPONSE FROM: '+server.port)
                print(response)
    
    def sendReadRequest(self, id):
        server_list = self.getReadQuorum()
        
        latest_timestamp = 0
        dt = datetime.fromtimestamp(latest_timestamp)
        final_respone = ''
        deleted = False
        for server in server_list:
            with grpc.insecure_channel('localhost:'+server.port) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                response = stub.read(server_pb2.ReadRequest(uuid=id))
                if response.status == 'SUCCESS':
                    dt_file = datetime.strptime(response.timestamp, "%d/%m/%Y %H:%M:%S")
                    if dt_file>dt:
                        dt = dt_file
                        deleted = False
                        final_respone = response
                elif response.status == 'FILE ALREADY DELETED':
                    dt_file = datetime.strptime(response.timestamp, "%d/%m/%Y %H:%M:%S")
                    if dt_file>dt:
                        dt = dt_file
                        deleted = True
                        final_respone = response
                else:
                    continue
                
        print(final_respone)
                        
    def sendWriteRequest(self, content, filename, id):
        server_list = self.getWriteQuorum()
        
        for server in server_list:
            with grpc.insecure_channel('localhost:'+server.port) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                response = stub.write(server_pb2.WriteRequest(name=filename, content=content, uuid=id))
                print('RESPONSE FROM: '+server.port)
                print(response)

    def sendDeleteRequest(self, ids):
        server_list = self.getWriteQuorum()
        
        for server in server_list:
            with grpc.insecure_channel('localhost:'+server.port) as channel:
                stub = server_pb2_grpc.ServerStub(channel)
                response = stub.delete(server_pb2.DeleteRequest(uuid=ids))
                print('RESPONSE FROM: '+server.port)
                print(response)
        
def loop():
    while True:
        print('1. Read Request')
        print('2. Write Request')
        print('3. Delete Request')
        print('4. Get Server List')
        print('5. Exit')
        client = Client(str(uuid.uuid4()))
        
        choice = int(input('Enter your choice: '))
        if choice == 1:
            ids = str(input('Enter UUID: '))
            client.sendReadRequest(ids)
        elif choice == 2:
            content = str(input("Enter Content: "))
            filename = str(input("Enter Filename: "))
            choice = str(input('Press 1 for Creating NEW FILE, Press 2 for Updating Existing File: '))
            id = None
            if choice == '1':
                id = str(uuid.uuid4())
            else:
                id = str(input("Enter UUID: "))
            client.sendWriteRequest(content, filename, id)
            pass
        elif choice == 3:
            ids = str(input('Enter UUID: '))
            client.sendDeleteRequest(ids)
            pass
        elif choice == 4:
            client.getServerList()
            pass
        elif choice == 5:
            break

def test():
    client = Client(str(uuid.uuid4()))

    print("Test Case 1: Get Server List")
    client.getServerList()

    print("Test Case 2: Write Request")
    id = str(uuid.uuid4())
    client.sendWriteRequest('Hello World', 'test.txt', id)
    
    print("Test Case 3: Read Request from datastore")
    client.sendReadRequest(id)
    
    print("Test Case 3.1: Read Request from each replica")
    client.sendAllReadRequest(id)
    
    print("Test Case 4: Update File Request")
    client.sendWriteRequest('Hello World updated', 'test.txt', id)
    
    print("Test Case 5: Read Request After Update")
    client.sendReadRequest(id)
    
    print("Test Case 5.1: Read Request After Update all replicas")
    client.sendAllReadRequest(id)
    
    print("Test Case 6: Delete Request")
    client.sendDeleteRequest(id)
    
    print("Test Case 7: Read Request After Delete")
    client.sendReadRequest(id)
    
    print("Test Case 7.1: Read Request After Delete all replicas")
    client.sendAllReadRequest(id)
    
    print("Test Case 8: Same File Update Request After Delete")
    client.sendWriteRequest('Hello World-2', 'test.txt', id)
    
    print("Test Case 9: Delete Request After Delete")
    client.sendDeleteRequest(id)

if __name__=="__main__":
    print(sys.argv)
    if sys.argv[1]=='run':
        loop()
    elif sys.argv[1]=='test':
        test()
    pass