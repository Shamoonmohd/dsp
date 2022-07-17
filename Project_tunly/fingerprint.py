import scipy.signal as signal
import librosa    
import numpy as np
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage import (generate_binary_structure, iterate_structure)

# This function calculate the fingerprint of the audio signal
# to be used for analysis
def fingerprint(wav_file, recorded):    
    if recorded == 1:
        wav = np.transpose(wav_file)
        fs = 8000
    else:
        wav, fs = librosa.load(wav_file, sr=8000, mono=True)
    
    y_f, x_t, z_stft = signal.stft(wav, fs=fs, window='boxcar', nperseg=1000)
    
    z_abs = np.abs(z_stft)/np.max(np.abs(z_stft))
    
    size = 5  
    s = generate_binary_structure(2, 2)
    partition = iterate_structure(s, size) 
    z_local = maximum_filter(z_abs, footprint=partition) 
    
    z = (z_abs == z_local)
    z = np.array(z, dtype=int)

    return z
    