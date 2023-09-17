import joblib
from sklearn.ensemble import *
import pyrpde
import antropy
import librosa
import numpy as np
import scipy
from scipy.signal import find_peaks

def predict_park_from_audio(audio_path):
    #!pip3 install scikit-learn==1.0.2
    filename = "./rf.joblib"
    loaded_model = joblib.load(open(filename, 'rb'))
    #!pip3 install pyrpde
    #!pip3 install antropy
    file = librosa.load(audio_path)
    #print(file[0])
    #print(pyrpde.rpde(np.array([0.8,0.2,-0.3,-0.1]).astype(np.float32),tau=50))
    num_Pulses = len(find_peaks(file[0])[0])
    #num_Pulses = 4000
    DFA = antropy.detrended_fluctuation(file[0])
    #DFA = 0.55
    
    return(loaded_model.predict_proba([[DFA, num_Pulses]])[0][1])
    #what do I return?

'''
audio_path = './audio/audio_20230917075556.wav'
print("answer: ", predict_emotion_from_audio(audio_path))
'''