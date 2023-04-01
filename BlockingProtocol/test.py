import stat
from time import sleep
from client import testCase
import server
import registryServer
from multiprocessing import Process
import os
import shutil

def deleteDirectory(filename):
    for file in filename:
        if os.path.exists('files/'+file):
            os.chmod('files/'+file, stat.S_IWUSR)
            shutil.rmtree('files/'+file)

if __name__=="__main__":
    server_name = ['server1', 'server2', 'server3', 'server4', 'server5', 
                   'server6', 'server7', 'server8', 'server9', 'server10']
    server_port = ['5001', '5002', '5003', '5004', '5005', '5006', '5007', '5008', '5009', '5010']
    deleteDirectory(os.listdir('files'))
    p = Process(target=registryServer.main)
    p.start()
    sleep(3)
    servers = []
    for i in range(10):
        p1 = Process(target=server.main, args=(server_name[i], server_port[i]))
        servers.append(p1)
        p1.start()
        sleep(2)
    sleep(1)
    testCase()
    print("\nTest Completed\n")
    for i in range(10):
        servers[i].terminate()
    p.terminate()

    
