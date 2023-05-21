from client import *

cli = Client('127.0.0.1')
cli.TryConnection()
cli.SendData(str.encode('Dados Maneiros'))
print(cli.ReceiveData().decode())