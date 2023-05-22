import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

#retorna fig do grafico
def Show2B1Q(window,array2b1q=[]):
    fig,ax=plt.subplots(figsize=(8,4)) #Faz subplot
    lenght =len(array2b1q) #Tamanho de Array
    n = 200 #samples por bit
    bit_duration=1 #duração em s do bit
    bit_time= np.linspace(0,bit_duration,n,endpoint=False) # tempo de 1 bit
    wave=np.array([]) #onda inicialização
    for i in array2b1q:
        bit_data= np.array([i]*n) #coloca o valor do array na posição n vezes
        wave = np.concatenate((wave,bit_data)) #concatena
    time = np.arange(0,lenght*bit_duration,bit_duration/n)
    ax.plot(time,wave) #plota
    ax.set(xlabel='Tempo',ylabel='Volts',title='2B1Q')
    return fig