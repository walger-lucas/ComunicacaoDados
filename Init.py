import tkinter as tk
import server as srv
import client as cli
import socket
from PIL import ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Graph import *
from BinFuncs import *


server = None
client = None
canvas = None
def close_window():
    print('Janela fechando')
    if(server!=None):
        server.CloseConnection()
    if(client!=None):
        client.skt.close
    window.destroy()
def selection_handle(selection):
    global isServer
    if(selection == 'Server'):
        isServer=True
    elif selection =='Client':
        isServer=False

def Iniciar():
    
    global server,client,isServer
    text = entryId.get()
    ip_frame.pack_forget()
    text_frame.pack()
    #Seta se será server ou cliente, e remove coisas desnecessárias
    if(isServer==True):
        server = srv.Server(text)
        server.ListenAndWaitConnection()
        window.geometry('400x170')
    else:
        client = cli.Client(text)
        client.TryConnection()
        text_label.pack_forget()
        text_entry.pack_forget()
        text_button.pack_forget()
        Receive()

def Send():
    global canvas
    text = text_entry.get()
    text_text.config(text="Texto: "+text)
    
    binary_array = ToBinary(text)
    cript_array = binary_array #MUDAR QUANDO HAVER CRIPTOGRAFIA
    lineCode_array = Encode2B1Q(cript_array)
    text_bin.config(text='Binário: '+ArrayBitsToStringBits(binary_array))
    text_cript.config(text='Criptografado: '+ArrayBitsToStringBits(cript_array))
    text_lineCode.config(text='2B1Q (V): '+str(lineCode_array))
    pack = PackData(lineCode_array)
    server.SendData(pack)
    
    
    if(canvas!=None):
        canvas.get_tk_widget().destroy()
    canvas = Show2B1Q(text_frame,lineCode_array)
    window.geometry('400x500')
#Tenta receber os dados e mostrá-los em tela a cada 200ms.
def Receive():
    global canvas
    try:
        pack = client.ReceiveData()
        if(pack):
            lineCode_array = UnpackData(pack)
            cript_array = Decode2B1Q(lineCode_array)
            binary_array = cript_array
            text = ToString(binary_array)
            text_text.config(text="Texto: "+text)
            text_bin.config(text='Binário: '+ArrayBitsToStringBits(binary_array))
            text_cript.config(text='Criptografado: '+ArrayBitsToStringBits(cript_array))
            text_lineCode.config(text='2B1Q (V): '+str(lineCode_array))
            if(canvas!=None):
                canvas.get_tk_widget().destroy()
            canvas = Show2B1Q(text_frame,lineCode_array)
            window.geometry('400x500')
    except socket.timeout:
        window.update()
    
    window.after(200,Receive)
            

            
        
    
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



