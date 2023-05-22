import tkinter as tk
import socket
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graph import *
from BinFuncs import *

PORT = 55555
host = 'localhost'
server = None
client = None
canvas,fig = None,None
conn, ender = None, None
isConnected,isRunning = False, True
lineCodeArray = []

#Mostra o Gráfico se houver data a mostrar, caso tenha mostrado, retira de coisas a mostrar
def ShowLineCode():
    global isRunning,lineCodeArray,canvas,fig
    if lineCodeArray!=[]:
        if(canvas!=None):
            canvas.get_tk_widget().destroy()
        if(fig):
            plt.close(fig)
        fig = Show2B1Q(text_frame,lineCodeArray)
        canvas = FigureCanvasTkAgg(fig,text_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        lineCodeArray=[]

    if(isRunning):
        window.after(200,ShowLineCode)


#Fecha Janela
def close_window():
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

#Seleção de Cliente ou Server
def selection_handle(selection):
    global isServer
    if(selection == 'Server'):
        isServer=True
    elif selection =='Client':
        isServer=False
#Espera conexão do servidor
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

#Botão de conexão, prepara em caso de Server ou Client
def Iniciar():
    global server,client,isServer,host
    host = entryId.get()
    ip_frame.pack_forget()
    text_frame.pack()
    ShowLineCode()
    window.update()
    #Seta se será server ou cliente, e remove coisas desnecessárias
    if(isServer==True):
        try:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP
            server.settimeout(5) #5s de timeout
            server.bind((host,PORT))
            server.listen()
            thread1 = threading.Thread(target=WaitConnection)
            thread1.start()
            window.geometry('400x170')
        except:
            close_window()
    else:
        client= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        text_label.pack_forget()
        text_entry.pack_forget()
        text_button.pack_forget()
        thread2 = threading.Thread(target=Receive)
        thread2.start()
    

def Send():
    global canvas, isConnected, fig, lineCodeArray
    text = text_entry.get()
    text_text.config(text="Texto: "+text)
    
    binary_array = ToBinary(text)
    cript_array = binary_array #MUDAR QUANDO HAVER CRIPTOGRAFIA
    lineCode_array = Encode2B1Q(cript_array)
    text_bin.config(text='Binário: '+ArrayBitsToStringBits(binary_array))
    text_cript.config(text='Criptografado: '+ArrayBitsToStringBits(cript_array))
    text_lineCode.config(text='2B1Q (V): '+str(lineCode_array))
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
#Tenta receber os dados e mostrá-los em tela a cada 200ms.
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
                lineCode_array = UnpackData(pack)
                cript_array = Decode2B1Q(lineCode_array)
                binary_array = cript_array
                text = ToString(binary_array)
                text_text.config(text="Texto: "+text)
                text_bin.config(text='Binário: '+ArrayBitsToStringBits(binary_array))
                text_cript.config(text='Criptografado: '+ArrayBitsToStringBits(cript_array))
                text_lineCode.config(text='2B1Q (V): '+str(lineCode_array))
                window.geometry('400x500')
                lineCodeArray=lineCode_array

        except:
            pass
     
window = tk.Tk()

window.geometry('400x130')

window.protocol('WM_DELETE_WINDOW',close_window)


#Tela inicial
ip_frame = tk.Frame(window)
selected_option = tk.StringVar()
selected_option.set('Server')
isServer=True

options=tk.OptionMenu(ip_frame,selected_option,"Server","Client",command=selection_handle)
label = tk.Label(ip_frame,text='IPV4:')
entryId = tk.Entry(ip_frame)
entryId.insert(0,'127.0.0.1')
buttonAccept=tk.Button(ip_frame,text='Conectar',command=Iniciar)


#Tela de adição de dados Envio
text_frame = tk.Frame(window)
text_label = tk.Label(text_frame,text='Adicione a palavra a enviar')
text_entry = tk.Entry(text_frame)
text_text = tk.Label(text_frame,text='Texto: ')
text_bin= tk.Label(text_frame,text='Binário: ')
text_cript=tk.Label(text_frame,text='Criptogradado: ')
text_lineCode = tk.Label(text_frame,text='2B1Q (V) : ')
text_button = tk.Button(text_frame,text='Enviar',command=Send)

text_label.pack()
text_entry.pack()
text_text.pack()
text_bin.pack()
text_cript.pack()
text_lineCode.pack()
text_button.pack()



options.pack()
label.pack()
entryId.pack()
buttonAccept.pack()
ip_frame.pack()
window.mainloop()



