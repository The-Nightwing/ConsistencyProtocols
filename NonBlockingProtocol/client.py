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
                print("Host: "+server.host+", Port: "+server.port)

    def sendReadRequest(self, port, ids):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.read(server_pb2.ReadRequest(uuid = ids))
            print(response.status)
            if response.status == 'SUCCESS':
                print(response.content)
            print(response.timestamp)

    def sendWriteRequest(self, port, content, filename, id):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.writeClientRequest(server_pb2.WriteRequest(uuid = id, content=content,  name=filename))
            print("Status: "+response.status+ ", UUID: "+id)

    def sendDeleteRequest(self, port, ids):
        with grpc.insecure_channel('localhost:'+port) as channel:
            stub = server_pb2_grpc.ServerStub(channel)
            response = stub.deleteClientRequest(server_pb2.DeleteRequest(uuid = ids))
            print(response.status)
        
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
            server_port = str(input('Enter server port: '))
            ids = str(input('Enter UUID: '))
            client.sendReadRequest(server_port, ids)
        elif choice == 2:
            server_port = str(input('Enter Client port: '))
            content = str(input("Enter Content: "))
            filename = str(input("Enter Filename: "))
            choice = str(input('Press 1 for Creating NEW FILE, Press 2 for Updating Existirng File: '))
            id = None
            if choice == '1':
                id = str(uuid.uuid4())
            else:
                id = str(input("Enter UUID: "))
            client.sendWriteRequest(server_port, content, filename, id)
            pass
        elif choice == 3:
            server_port = str(input('Enter Client port: '))
            ids = str(input('Enter UUID: '))
            client.sendDeleteRequest(server_port, ids)
            pass
        elif choice == 4:
            client.getServerList()
            pass
        elif choice == 5:
            break

def testCase():
    client = Client(str(uuid.uuid4()))

    print("\nTest Case 1: Get Server List \n")
    client.getServerList()

    print("\nTest Case 2: Write Request \n")
    id = str(uuid.uuid4())
    port = '5001'
    client.sendWriteRequest(port, 'Hello World', 'test.txt', id)
    
    print("\nTest Case 3: Read Request")
    print("\nFrom Server 1:")
    client.sendReadRequest(port, id)
    print("\nFrom Server 2:")
    client.sendReadRequest("5002", id)
    print("\nFrom Server 3:")
    client.sendReadRequest("5003", id)
    print("\nFrom Server 4:")
    client.sendReadRequest("5004", id)
    print("\nFrom Server 5:")
    client.sendReadRequest("5005", id)
    
    time.sleep(1)
    print("\nTest Case 4: Update File Request \n")
    client.sendWriteRequest(port, 'Hello World updated', 'test.txt', id)
    
    print("\nTest Case 5: Read Request After Update")
    print("\nFrom Server 1:")
    client.sendReadRequest(port, id)
    print("\nFrom Server 2:")
    client.sendReadRequest("5002", id)
    print("\nFrom Server 3:")
    client.sendReadRequest("5003", id)
    print("\nFrom Server 4:")
    client.sendReadRequest("5004", id)
    print("\nFrom Server 5:")
    client.sendReadRequest("5005", id)
    
    time.sleep(1)
    print("\nTest Case 6: Delete Request \n")
    client.sendDeleteRequest(port, id)
    
    print("\nTest Case 7: Read Request After Delete \n")
    client.sendReadRequest(port, id)
    
    print("\nTest Case 8: Same File Update Request After Delete \n")
    client.sendWriteRequest(port, 'Hello World-2', 'test.txt', id)
    
    print("\nTest Case 9: Delete Request After Delete \n")
    client.sendDeleteRequest(port, id)
    return

if __name__=="__main__":
    loop()
    pass