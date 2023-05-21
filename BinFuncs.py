import struct
#Transforma palavra em array de bit e uma string de bits que representa a palavra em ascii
def ToBinary(word):
    l =[]
    bits_string =''
    for i in word:
        l.append(ord(i))
    for i in l:
        bits_string+=i
    bits_array= []
    for i in bits_string:
        bits_array.append(int(i))

    return bits_array

def ArrayBitsToStringBits(bits_array=[]):
    s=''
    for i in bits_array:
        s+=str(i)
    return s

    


ENCONDING_2B1Q_NEG=[-1,-3,1,3] #Tensão para cada indexador 00: -3, 01: -1, 10: 1, 11:3, em caso do último ser negativo
ENCONDING_2B1Q_POS=[1,3,-1,-3] #Tensão para cada indexador 00: 3, 01: 1, 10: -1, 11:-3, em caso do último ser positivo
#Necessita de um numero par de bits, então adiciona 0 no final caso seja impar.
#Encoda em 2B1Q
def Encode2B1Q(binary_array=[]):
    b_array =[]
    if (len(binary_array) % 2 == 1):
        binary_array.append('0')
    positivo=True
    for i in range(0,len(binary_array),2):
        
        number_int = binary_array[i]*2+binary_array[i+1]
        
        voltage = 0
        if positivo:
            voltage = ENCONDING_2B1Q_POS[number_int]
        else:
            voltage = ENCONDING_2B1Q_NEG[number_int]
        if voltage>0:
            positivo=True
        else:
            positivo=False
        b_array.append(voltage)
    return b_array
    
#Gera um array de bits a partir de um array no line code 2b1q
def Decode2B1Q(data2b1q=[]):
    h=[]
    positivo = True
    for i in data2b1q:
        if positivo:
            if i==-3:
                h.append(1)
                h.append(1)
            elif i==-1:
                h.append(1)
                h.append(0)
            elif i==3:
                h.append(0)
                h.append(1)
            elif i==1:
                h.append(0)
                h.append(0)
        else:
            if i==3:
                h.append(1)
                h.append(1)
            elif i==1:
                h.append(1)
                h.append(0)
            elif i==-3:
                h.append(0)
                h.append(1)
            elif i==-1:
                h.append(0)
                h.append(0)
        if i>0:
            positivo = True
        else:
            positivo = False
    return h

#Empacota dados em uma forma enviável pela socket
def PackData(data=[]):
    pack= struct.pack('!{}i'.format(len(data)),*data)
    return pack

#Desempacota dados em uma forma enviável pela socket
def UnpackData(pack):
     data= struct.unpack('!{}i'.format(len(pack)//4),pack)
     return data