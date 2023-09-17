import scipy
import tensorflow as tf
import numpy as np
import librosa
from keras.models import load_model

def predict_emotion_from_audio(audio_path):
    val = []
    features = 52
    
    # Load and process the audio file
    data_x, sampling_rate = librosa.load(audio_path, res_type='kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(y=data_x, sr=sampling_rate, n_mfcc=features).T, axis=0)
    val.append(mfccs)
    val = np.expand_dims(val, axis=1)
    val = np.swapaxes(val, 1, 2)
    val = np.resize(val, (1, 58, 1))
    
    # Normalize the data
    for i in range(len(val)):
        val[i] = (val[i] + 4.05214) / 51.821
    
    # Load the trained model and predict
    model = tf.keras.models.load_model('/Users/anish/BioAcoustix/backend/model.h5')
    #print(model.summary())
    classes = ["angry", "calm", "disgust", "fear", "happy","neutral","sad","surprise"]
    #print(model.predict(val))
    probabilities = scipy.special.softmax(model.predict(val))[0]
    
    # Create a list of tuples with class and its probability
    results = list(zip(classes, probabilities))
    
    return results

# Example usage:
'''
audio_path = '/Users/anish/BioAcoustix/backend/audio/audio_20230916231214.wav'
model_path = '/Users/anish/BioAcoustix/backend/model.h5'
predictions = predict_emotion_from_audio(audio_path)
for emotion, prob in predictions:
    print(f"{emotion}: {prob}")
'''

#0.2797080874443054
#0.2797080874443054