"""
Demo of how to use the respiratory model
dir_ is path to sample respiratory wav
"""
import scipy
import tensorflow as tf
import keras
import numpy as np
import librosa
val=[]
dir_= './104_1b1_Pl_sc_Litt3200.wav'
features = 52
#input must be shape (58, 1, 1)
data_x, sampling_rate = librosa.load(dir_,res_type='kaiser_fast')
mfccs = np.mean(librosa.feature.mfcc(y=data_x, sr=sampling_rate, n_mfcc=features).T,axis=0)
val.append(mfccs)
val = np.expand_dims(val,axis=1)
# Create a new model instance
from keras.models import load_model
model = tf.keras.models.load_model('./model.h5')
classes = ["COPD" ,"Bronchiolitis ", "Pneumoina", "URTI", "Healthy"]

for i in zip(classes,scipy.special.softmax(model.predict(val))[0][0]):
    print(i)
