import struct

# Transforma palavra em array de bit e uma string de bits que representa a palavra em ascii
def ToBinary(word):
    l =[]
    bitsString =''
    for i in word:
        l.append(bin(ord(i))[2:].zfill(8))
    for i in l:
        bitsString+=i
    bitsArray= []
    for i in bitsString:
        bitsArray.append(int(i))

    return bitsArray

# Transforma de array de bits para string de bits
def ArrayBitsToStringBits(bitsArray=[]):
    s=''
    for i in bitsArray:
        s+=str(i)
    return s

# Transforma de bits para string
def ToString(binArray=[]):
    text =''
    for i in range(0,len(binArray),8):
        text+= chr(binArray[i]*128+binArray[i+1]*64+binArray[i+2]*32+binArray[i+3]*16+binArray[i+4]*8+binArray[i+5]*4+binArray[i+6]*2+binArray[i+7]*1)
    return text


## 2B1Q ENCODER DECODER 

ENCONDING_2B1Q_NEG=[-1,-3,1,3] # Tensão para cada indexador 00: -3, 01: -1, 10: 1, 11:3, em caso do último ser negativo
ENCONDING_2B1Q_POS=[1,3,-1,-3] # Tensão para cada indexador 00: 3, 01: 1, 10: -1, 11:-3, em caso do último ser positivo
# Necessita de um numero par de bits, então adiciona 0 no final caso seja impar.
# Encoda em 2B1Q
def Encode2B1Q(binaryArray=[]):
    resultArray =[]
    if (len(binaryArray) % 2 == 1):
        binaryArray.append('0')
    positivo=True
    for i in range(0,len(binaryArray),2):
        number_int = binaryArray[i]*2+binaryArray[i+1]
        voltage = 0
        if positivo:
            voltage = ENCONDING_2B1Q_POS[number_int]
        else:
            voltage = ENCONDING_2B1Q_NEG[number_int]
        if voltage>0:
            positivo=True
        else:
            positivo=False
        resultArray.append(voltage)
    return resultArray
    
# Gera um array de bits a partir de um array no line code 2b1q
def Decode2B1Q(data2b1q=[]):
    result=[]
    positivo = True
    for i in data2b1q:
        if positivo:
            if i==-3:
                result.append(1)
                result.append(1)
            elif i==-1:
                result.append(1)
                result.append(0)
            elif i==3:
                result.append(0)
                result.append(1)
            elif i==1:
                result.append(0)
                result.append(0)
        else:
            if i==3:
                result.append(1)
                result.append(1)
            elif i==1:
                result.append(1)
                result.append(0)
            elif i==-3:
                result.append(0)
                result.append(1)
            elif i==-1:
                result.append(0)
                result.append(0)
        if i>0:
            positivo = True
        else:
            positivo = False
    return result

## Empacotamento e Desempacotamento de Dados

# Empacota dados em uma forma enviável pela socket
def PackData(data=[]):
    pack= struct.pack('!{}i'.format(len(data)),*data)
    return pack

# Desempacota dados em uma forma enviável pela socket
def UnpackData(pack):
     data= struct.unpack('!{}i'.format(len(pack)//4),pack)
     return data