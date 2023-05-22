import socket

class Client:
    def __init__(self, HOST='127.0.0.1',PORT=55556):
        self.HOST = HOST
        self.PORT = PORT
        self.skt= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.isConnected = False
        self.skt.settimeout(1)
    
    def TryConnection(self):
        if(not self.isConnected):
            self.skt.connect((self.HOST,self.PORT))
            print('Conexão estabelecida em: {}:{}'.format(self.HOST,self.PORT))
            self.isConnected = True
        else:
            print('Já conectado a {}:{}, desconecte-se antes de tentar conexão novamente.'.format(self.HOST,self.PORT))
    
    def SendData(self,data):
        if( self.isConnected):
            self.skt.send(data)
            print('Dados enviados para {}:{}'.format(self.HOST,self.PORT))
        else:
            print('Não consegue-se enviar dados sem conexão.')
    
    def ReceiveData(self,size=1024):
        if( self.isConnected):
            data = self.skt.recv(size)
            if(data):
                print('Dados recebidos de {}:{}'.format(self.HOST,self.PORT))
            return data
        else:
            print('Não consegue-se enviar dados sem conexão.')
        