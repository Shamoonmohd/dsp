import sys
import sounddevice as sd
import soundfile as sf
import pickle
import tkinter as tk
import tkinter.messagebox
import numpy as np
import queue
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot
import multiprocessing
import pyaudio
import struct

from analyzer import analyzer
from db import init_database

try:
    with open('database.pickle', 'rb') as f:
        database = pickle.load(f)
except:
    init_database()
    with open('database.pickle', 'rb') as f:
        database = pickle.load(f)


def capturing(time, input_index, output_index):
    print(f'inputindex {input_index}')
    print(f'outputindex {output_index}')
    #sd.default.device = input_index,output_index
    sd.default.device = 1,1
    sd.default.channels = 1,12
    
    fs = 8000
    
    print('Recording the Input..')
    
    sample = sd.rec(int(time * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait() 
    sample = np.array(sample)
    #print(f'sample{sample}')
    sample = sample.flatten()
    
    print('Done recording!')
    
    return sample


input_index = 0
output_index = 0

#Function to capture and analyze the audio signal
#Implement GUI using TKinter
def drawGUI():

    def buttonClick():
        input_index = inputVar.get()
        output_index = outputVar.get()
        print(f'inputVar {inputVar.get()}')
        print(f'outputVar {outputVar.get()}')
        
        try:
            #Capturing the audio signal
            sample = capturing(10, input_index, output_index)
            global result
            #Analyzing the input signal using correlation(Default device is 1)
            result = analyzer(sample, 1)
            title = result[0]
            
            if title != 'NOT a Match':
                print(f'Its a match!')
                tk.messagebox.showinfo('Yay! It\'s a match!', title)
            else:
                print(f'No match :(')
        except:
            print(f'ERROR!')
    
    #Title for GUI
    window = tk.Tk()
    window.title('Tune.ly')

    mainFrame = tk.Frame()
    mainFrame.pack()

    padding0 = tk.Label(
        text="", 
        master=mainFrame,
        height=1,
    )
    padding0.pack()
    
    nameLbl = tk.Label(
        text="                            Tune.ly                            ",
        height=2,
        font=(None, 36),
        master=mainFrame,
    )
    nameLbl.pack()

    titleLbl = tk.Label(
        text="              DSP-Lab 2022 Final Project              ",
        height=2,
        font=(None, 18),
        master=mainFrame,
    )
    titleLbl.pack()

    descLbl = tk.Label(
        text="Recognize music with fingerprinting and Correlation",
        font=(None, 16),
        master=mainFrame
    )
    descLbl.pack()

    padding1 = tk.Label(
        text="", 
        master=mainFrame,
        height=2,
    )
    padding1.pack()

    inputMenuLbl = tk.Label(
        text="SELECT INPUT DEVICE",
        master=mainFrame,
    )
    inputMenuLbl.pack()

    #Query available devices connected to the sound card
    devices = sd.query_devices()
    devices_str = [0]*len(devices)
            
    for i in np.arange(len(devices)):
        device_i = devices[i]
        devices_str[i] = device_i['name']

    inputVar = tk.StringVar(mainFrame)
    inputMenu = tk.OptionMenu(mainFrame, inputVar, *devices_str)
    inputMenu.pack()

    padding2 = tk.Label(
        text="", 
        master=mainFrame,
        height=1,
    )
    padding2.pack()
    
    outputMenuLbl = tk.Label(
        text="SELECT OUTPUT DEVICE",
        master=mainFrame,
    )
    outputMenuLbl.pack()

    outputVar = tk.StringVar(mainFrame)
    ouputMenu = tk.OptionMenu(mainFrame, outputVar, *devices_str)
    ouputMenu.pack()

    padding3 = tk.Label(
        text="", 
        master=mainFrame,
        height=1,
    )
    padding3.pack()

    button = tk.Button(
        text="START",
        width=25,
        height=2,
        font=(None, 16),
        relief=tk.RAISED,
        master=mainFrame,
        command=buttonClick
    )
    button.pack()

    padding4 = tk.Label(
        text="", 
        master=mainFrame,
        height=2,
    )
    padding4.pack()

    window.mainloop()

#Funtion to plot the input signal to be analyzed in real time
#Can be useful to graphically anlayze the input signal
#Pyaudio is used to read the input from selected device and
#plot it in real time using matplotlib
def liveGraph():
    WIDTH = 2           # bytes per sample
    CHANNELS = 1        # mono
    RATE = 8000         # frames per second
    BLOCKLEN = 1024     # block length in samples
    DURATION = 1000       # Duration in seconds

    K = int( DURATION * RATE / BLOCKLEN )   # Number of blocks

    print('Block length: %d' % BLOCKLEN)
    print('Number of blocks to read: %d' % K)
    print('Duration of block in milliseconds: %.1f' % (1000.0 * BLOCKLEN/RATE))

    # Set up plotting...

    pyplot.ion()           # Turn on interactive mode
    pyplot.figure(1)
    [g1] = pyplot.plot([], [], 'blue')  # Create empty line

    n = range(0, BLOCKLEN)
    pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
    pyplot.xlabel('Time (n)')
    g1.set_xdata(n)                   # x-data of plot (discrete-time)

    pyplot.ylim(-10000, 10000)        # set y-axis limits

    # Open the audio stream

    p = pyaudio.PyAudio()
    PA_FORMAT = p.get_format_from_width(WIDTH)
    stream = p.open(
        format = PA_FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        output = False)

    # Read microphone, plot audio signal

    for i in range(K):

        # Read audio input stream
        input_bytes = stream.read(BLOCKLEN)

        signal_block = struct.unpack('h' * BLOCKLEN, input_bytes)

        g1.set_ydata(signal_block)   # Update y-data of plot
        pyplot.pause(0.0001)

    stream.stop_stream()
    stream.close()
    p.terminate()

    pyplot.ioff()           # Turn off interactive mode
    pyplot.show()           # Keep plot showing at end of program
    pyplot.close()

    print('* Finished')


if __name__ == '__main__':
    
    #Process for GUI using tkinter
    p1 = multiprocessing.Process(target=drawGUI)

    #Process to display real time graph of input audio to be analyzed
    p2 = multiprocessing.Process(target=liveGraph)
    
    #joining both processes to main
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
    
    