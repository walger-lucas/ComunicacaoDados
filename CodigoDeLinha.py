import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import socket
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from BinaryFunctions import *

## Gráfico

# Retorna fig do grafico
def Show2B1Q(array2b1q=[]):
    fig,ax = plt.subplots(figsize=(8,4)) # Faz subplot
    lenght = len(array2b1q) # Tamanho de Array
    n = 200 # Samples por bit
    bitDuration = 1 # Duração em s do bit
    wave = np.array([]) # Onda inicialização
    for i in array2b1q:
        bitData = np.array([i]*n) # Coloca o valor do array na posição n vezes
        wave = np.concatenate((wave,bitData)) # Concatena
    time = np.arange(0,lenght*bitDuration,bitDuration/n)
    ax.plot(time,wave) # Plota
    ax.set(xlabel='Tempo',ylabel='Volts',title='2B1Q')
    return fig

# Mostra o Gráfico se houver data a mostrar, caso tenha mostrado, retira de coisas a mostrar
def ShowLineCode():
    global isRunning,lineCodeArray,canvas,fig

    if lineCodeArray!=[]:
        if(canvas!=None):
            canvas.get_tk_widget().destroy()
        if(fig):
            plt.close(fig)
        
        fig = Show2B1Q(lineCodeArray)
        canvas = FigureCanvasTkAgg(fig,textFrame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        lineCodeArray=[]
    # Seta próxima atualização para aqui 200ms
    if(isRunning):
        window.after(200,ShowLineCode)

# Fecha Janela
def CloseWindow():
    global isRunning
    print('Janela fechando')
    isRunning= False
    try:
        if(canvas):
            canvas.get_tk_widget().destroy()
        if(fig):
            plt.close(fig)
        if(server):
            server.close()
        if(client):
            client.close()
    except:
        print("error")
        pass
    window.destroy()

# Seleção de Cliente ou Server
def selectionHandle(selection):
    global isServer
    if(selection == 'Server'):
        isServer=True
    elif selection =='Client':
        isServer=False
# Espera conexão do servidor
def WaitConnection():
    global conn, ender,server,isConnected
    while(isConnected==False and isRunning==True):
        try:
            print('Tentando Conectar')
            conn,ender = server.accept()
            isConnected = True
            print('Conectou-se')
            break
        except: 
            isConnected = False
            print("Nao conseguiu conexoes.")

# Botão de conexão, prepara em caso de Server ou Client
def Iniciar():
    global server,client,isServer,host
    host = entryId.get()
    ipFrame.pack_forget()
    textFrame.pack()
    ShowLineCode()
    window.update()
    # Seta se será server ou cliente, e remove coisas desnecessárias
    if(isServer==True):
        try:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP
            server.settimeout(5) # 5s de timeout
            server.bind((host,PORT))
            server.listen()
            thread1 = threading.Thread(target=WaitConnection)
            thread1.start()
            window.geometry('400x170')
        except:
            CloseWindow()
    else:
        client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        textLabel.pack_forget()
        textEntry.pack_forget()
        textButton.pack_forget()
        thread2 = threading.Thread(target=Receive)
        thread2.start()
    
# Envia os dados, e atualiza o display
def Send():
    global canvas, isConnected, fig, lineCodeArray
    text = textEntry.get()
    textText.config(text="Texto: "+text)
    
    binaryArray = ToBinary(text)
    criptArray = binaryArray # MUDAR QUANDO HAVER CRIPTOGRAFIA
    lineCode_array = Encode2B1Q(criptArray)
    textBin.config(text='Binário: '+ArrayBitsToStringBits(binaryArray))
    textCript.config(text='Criptografado: '+ArrayBitsToStringBits(criptArray))
    textLineCode.config(text='2B1Q (V): '+str(lineCode_array))
    if isConnected:
        pack = PackData(lineCode_array)
        try:
            conn.send(pack)
        except:
            isConnected = False
            conn.close()
            print("Nao conseguiu enviar o pacote.")
    window.geometry('400x500')
    lineCodeArray=lineCode_array

# Tenta receber os dados e mostrá-los em tela a cada 200ms.
def Receive():
    global canvas, isConnected,fig,lineCodeArray
    
    while( (not isConnected) and isRunning):
        try:
            client.connect((host,PORT))
            isConnected=True
            print("Conectou-se")
        except: 
            print("Não conseguiu conectar")
    while(isConnected and isRunning):
        try:
            pack = client.recv(2048)
            if(pack):
                lineCodeArray = UnpackData(pack)
                criptArray = Decode2B1Q(lineCodeArray)
                binaryArray = criptArray
                text = ToString(binaryArray)
                textText.config(text="Texto: "+text)
                textBin.config(text='Binário: '+ArrayBitsToStringBits(binaryArray))
                textCript.config(text='Criptografado: '+ArrayBitsToStringBits(criptArray))
                textLineCode.config(text='2B1Q (V): '+str(lineCodeArray))
                window.geometry('400x500')
                lineCodeArray=lineCodeArray

        except:
            pass

# Inicialização de variaveis para servidor e outros
PORT = 55555
host = 'localhost'
server = None
client = None
canvas,fig = None,None
conn, ender = None, None
isConnected,isRunning = False, True
lineCodeArray = []

# Inicializacao da tela
window = tk.Tk()
window.geometry('400x130')
window.protocol('WM_DELETE_WINDOW',CloseWindow)

# Display da Tela inicial
ipFrame = tk.Frame(window)
selectedOption = tk.StringVar()
selectedOption.set('Server')
isServer=True # Booleano que controla seleção 
options=tk.OptionMenu(ipFrame,selectedOption,"Server","Client",command=selectionHandle)
label = tk.Label(ipFrame,text='IPV4:')
entryId = tk.Entry(ipFrame) # Entrada para IP
entryId.insert(0,'127.0.0.1')
buttonAccept=tk.Button(ipFrame,text='Conectar',command=Iniciar)

# Tela de adição de dados Envio
textFrame = tk.Frame(window)
textLabel = tk.Label(textFrame,text='Adicione a palavra a enviar')
textEntry = tk.Entry(textFrame)
textText = tk.Label(textFrame,text='Texto: ')
textBin= tk.Label(textFrame,text='Binário: ')
textCript=tk.Label(textFrame,text='Criptogradado: ')
textLineCode = tk.Label(textFrame,text='2B1Q (V) : ')
textButton = tk.Button(textFrame,text='Enviar',command=Send)

# Adição de itens ao Frame, tela inicial
textLabel.pack()
textEntry.pack()
textText.pack()
textBin.pack()
textCript.pack()
textLineCode.pack()
textButton.pack()

# Adição de itens ao Frame, tela secundária
options.pack()
label.pack()
entryId.pack()
buttonAccept.pack()

# Adição do frame inicial a window geral
ipFrame.pack()

# Inicialização do loop principal
window.mainloop()



