import subprocess
from server import output_filename
from scipy.io import wavfile

# Install the Whisper library from GitHub
subprocess.run(["pip", "install", "git+https://github.com/openai/whisper.git"])

# Install ffmpeg if you haven't already (you might need to install it differently on your operating system)
# You can run this command directly in your terminal outside of Python
# subprocess.run(["sudo", "apt", "update", "&&", "sudo", "apt", "install", "ffmpeg"])

# Run the Whisper command
audio_file = output_filename
model = "tiny.en"

result = subprocess.run(["whisper", audio_file, "--model", model], capture_output=True, text=True)

print(result.stdout)


#IBM Watson API
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, CategoriesOptions, ConceptsOptions, EmotionOptions, KeywordsOptions

authenticator = IAMAuthenticator('aVt_kq-t6KVyzdbh9DQQ8PdCjDjGbFeL4qVb-ftS2-Ca')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/ad3f9282-50fb-493a-83b7-63b62face7f2')

#Sentiment Analysis
transcription = result[0].split(']')[1:]

print(transcription)

response = natural_language_understanding.analyze(
    text = transcription,
    features=Features(keywords=KeywordsOptions(sentiment = True, emotion = True, limit=5))).get_result()

#sentiment analysis of the sentence
sentiment_dict = response["keywords"][0]["emotion"]
#Keys:
#sadness print(sentiment_dict['sadness'])
#joy
#fear
#disgust
#anger
