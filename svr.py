from server import *

print(socket.gethostname())
print(socket.gethostbyname(socket.gethostname()))
srv = Server('127.0.0.1')
srv.ListenAndWaitConnection()
while(srv.isConnected):
    data = srv.ReceiveData()
    if not data:
        srv.CloseConnection()
    else:
        print(data.decode())
        srv.SendData(data)