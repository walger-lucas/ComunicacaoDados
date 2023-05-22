import socket

class Server:
    # Construtor do Server
    def __init__(self, HOST='127.0.0.1',PORT=55556):
        self.HOST = HOST
        self.PORT = PORT
        self.isConnected=False
        self.skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.skt.bind((self.HOST,self.PORT))
        print('Socket aberta em {}:{}'.format(self.HOST,self.PORT))
    # Inicia processos de listen e criaçao de porta.
    def ListenAndWaitConnection(self):
        if(self.isConnected):
            print('Já Connectado em: {}.\n Finalize esta conexão antes de iniciar outra.'.format(self.ender))
        else:
            self.skt.listen()
            print('Aguardando conexão')
            self.conn,self.ender = self.skt.accept()
            print('Conexão em ',self.ender)
            self.isConnected=True
    def CloseConnection(self):
        if (self.isConnected):
            self.conn.close()
            self.skt.close()
            print('Conexão fechada em ', self.ender)
            self.isConnected=False
        else:
            print('Não há conexões para fechar.')
    def ReceiveData(self,size=1024):
        if (self.isConnected):
            data = self.conn.recv(size)
            return data
        else:
            print('Nenhuma conexao estabelecida para receber dados.')
    def SendData(self,data):
        if (self.isConnected):
            self.conn.send(data)
        else:
            print('Nenhuma conexao estabelecida para enviar dados.')



