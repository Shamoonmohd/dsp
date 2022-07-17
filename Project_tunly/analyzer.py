import numpy as np
from fingerprint import fingerprint
import scipy.signal as signal
from db import init_database
import pickle
import copy

#Function to analyze the input signal and audio database
#Fingerprint of input signal is correlated with audio wave files
#Pair with maximum correlation will resemble same genre
def analyzer(wav_file, recorded):        
    try:
        with open('database.pickle', 'rb') as f:
            database = pickle.load(f)
    except: 
        init_database()
        with open('database.pickle', 'rb') as f:
            database = pickle.load(f)
        
    audio_test = fingerprint(wav_file, recorded)
        
    corr = np.empty(6)
    
    for i in np.arange(6):
        audio_base_i = database[0][1][i]
        corr [i] = np.max(signal.correlate2d(audio_base_i, audio_test, mode='valid'))
    
    first_corr = np.max(corr)
    first_index = np.argmax(corr)
    
    aux_corr = copy.deepcopy(corr)
    aux_corr[first_index] = 0
    second_index = np.max(aux_corr)
    
    print(f'first max {first_corr} second max {second_index}')
    # Base conditions to check the valid correlated pair
    if first_corr >= 2.4*second_index or first_corr >= 20:
    # if first_corr >= 2.6*second_index or first_corr >= 8:
        song = database[0][0][first_index]
        song_path = database[0][2][first_index]      
    else:
        song = 'NO_MATCH'
        song_path = 0
    
    return song, song_path