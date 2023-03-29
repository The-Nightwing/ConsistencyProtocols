import grpc
import server_pb2
import server_pb2_grpc
import registryServer_pb2
import registryServer_pb2_grpc
import uuid
import time
import datetime


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
                print("host: "+server.host+" port: "+server.port)

    def sendReadRequest(self, port):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.read(server_pb2.ReadRequest(uuid = str(uuid.uuid4())))
            print(response.status)

    def sendWriteRequest(self, port):
        content = str(input("Enter Content: "))
        filename = str(input("Enter Filename: "))
        choice = str(input('Press 1 for Creating NEW FILE, Press 2 for Updating Existirng File:  '))
        id = None
        if choice == '1':
            id = str(uuid.uuid4())
        else:
            id = str(input("Enter UUID: "))

        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.writeClientRequest(server_pb2.WriteRequest(uuid = id, content=content,  name=filename))
            print("Status: "+response.status+ " uuid: "+response.uuid)

    def sendDeleteRequest(self, port):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.deleteClientRequest(server_pb2.DeleteRequest(uuid = str(uuid.uuid4())))
            print(response.status)
        
def loop():
    while True:
        print('1. Read Request')
        print('2. Write Request')
        print('3. Delete Request')
        print('4. Get Server List')
        client = Client(str(uuid.uuid4()))
        
        choice = int(input('Enter your choice: '))
        if choice == 1:
            server_port = str(input('Enter server port: '))
            client.sendReadRequest(server_port)
        elif choice == 2:
            server_port = str(input('Enter Client port: '))
            client.sendWriteRequest(server_port)
            pass
        elif choice == 3:
            server_port = str(input('Enter Client port: '))
            client.sendDeleteRequest(server_port)
            pass
        elif choice == 4:
            client.getServerList()
            pass

if __name__=="__main__":
    loop()
    pass