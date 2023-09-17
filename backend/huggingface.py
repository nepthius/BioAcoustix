# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("audio-classification", model="ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition")

# Create the pipeline
def predict_emotion_from_audio(audio_path):
    """
    Predict emotion from audio using a Hugging Face pipeline.
    
    Parameters:
    - audio_path (str): Path to the audio file.
    
    Returns:
    - dict: A dictionary with the predicted class and its score.
    """
    # Load the audio file
    with open(audio_path, "rb") as audio_file:
        input_audio = audio_file.read()

    # Use the pipeline to predict the emotion
    prediction = pipe(input_audio)

    return prediction

'''
# Example usage:
audio_path = "./audio/audio_20230917020903.wav"
emotion_prediction = predict_emotion_from_audio(audio_path)
print(emotion_prediction)
'''