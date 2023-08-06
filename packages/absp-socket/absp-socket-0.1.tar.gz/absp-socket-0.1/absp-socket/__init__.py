import socket

class connect:
    def __init__(self,host,port):
        self.host =host
        self.port  = port
    def server(self):
        host = self.host
        port = self.port
        
        server = socket.socket()
        server.bind((host, port))
        server.listen(5)
        while True:
            print("wating to the client connect!!! ")
            client, addr = server.accept()
            nick = client.recv(1024).decode("utf-8")
            print("client connected to name is : {nick} ")
            online = True
            while online:
                msg = client.recv(1024).decode("utf-8")
                print(f"client send msg is :    {msg}")
                if msg == "exit": 
                    online = False
                    exit()
                else:  
                    online = False
    def client(self):
       try:    
        host = self.host
        port = self.port            
        server = socket.socket()
        server.connect((host,port))    
        nick = input("enter nick name")
        server.send(nick.encode("utf-8"))   
        while True:
             msg = input("enter msg : ")
             server.send(msg.encode("utf-8"))  
             print(f"server msg send : {msg}" ) 
       except:
            print('server not start or error')