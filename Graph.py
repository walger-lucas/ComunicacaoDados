import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def Show2B1Q(window,array2b1q=[]):
    fig,ax=plt.subplots(figsize=(8,4))
    lenght =len(array2b1q)
    n = 200
    bit_duration=1
    bit_time= np.linspace(0,bit_duration,n,endpoint=False)
    wave=np.array([])
    for i in array2b1q:
        bit_data= np.array([i]*n)
        wave = np.concatenate((wave,bit_data))
    time = np.arange(0,lenght*bit_duration,bit_duration/n)
    ax.plot(time,wave)
    ax.set(xlabel='Tempo',ylabel='Volts',title='2B1Q')
    canvas = FigureCanvasTkAgg(fig,window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    return canvas