from huggingface import predict_emotion_from_audio
from flask import Flask, request, jsonify
from pydub import AudioSegment
import datetime
import os
import json
import traceback
import re
from parkinsons import predict_park_from_audio

import openai
import json
from dotenv import load_dotenv
import os
openai.api_key = os.getenv('OPENAI_KEY')
def chatGPT(GPTquery):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 1,
        max_tokens = 2000,
        messages = [
            { "role": "user","content": GPTquery}
        ]
    )
    
    return(response['choices'][0]['message']['content'])



app = Flask(__name__)

UPLOAD_FOLDER = './audio'
ALLOWED_EXTENSIONS = {'ogg', 'mp3', 'wav', 'm4a'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the request has an 'audio' file part
    if 'audio' not in request.files:
        app.logger.error("No audio file found in request")
        return jsonify({"error": "No audio file found"}), 400
    
    file = request.files['audio']

    # Check if the user did not select a file or if it's not allowed
    if file.filename == '' or not allowed_file(file.filename):
        app.logger.error("Invalid file name or format")
        return jsonify({"error": "Invalid file"}), 400

    if file:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        # Create a temporary filename for the uploaded file
        temp_filename = os.path.join(UPLOAD_FOLDER, "temp_audio." + file.filename.rsplit('.', 1)[1].lower())
        file.save(temp_filename)

        output_filename = os.path.join(UPLOAD_FOLDER, f"audio_{timestamp}.wav")
        print("output_filename: ", output_filename)

        try:
            # Convert the audio to wav format using pydub
            audio = AudioSegment.from_file(temp_filename)
            audio.export(output_filename, format="wav")

            # Clean up the temporary file
            os.remove(temp_filename)

            analysis_type = request.form.get('analysisType', None)  # Get the analysisType from the form data
            ddata = ""
            response_data = {}
            if analysis_type == 'emotion':
                
                data = predict_emotion_from_audio(output_filename)
                # No need to swap or convert anything here

                json_data = [{'emotion': item['label'], 'score': item['score']} for item in data]
                json_string = json.dumps(json_data, indent=2)
                print("jstring: ", json_string)
                
                emotionsDict = json.loads(json_string)

                # Assuming emotionsDict is the name of the list of dictionaries you shared
                top_two_emotions = emotionsDict[:2]

                # Extract the 'emotion' labels from the top two emotions
                first_emotion = top_two_emotions[0]['emotion']
                second_emotion = top_two_emotions[1]['emotion']

                # Construct the prompt string
                prompt = f"You are a physician that is apart of a tele health platform. In order to diagnose possible illnesses you listen to a patient's voice. The top two emotions that you hear are {first_emotion} and {second_emotion}. Determine any possible diagnosis/correlation to a diagnosis that you can make in order to help the patient. Only return a response/limit your response with only a numbered list of different diagnosis. Also go into 1-2 sentences in depth with each numbered point to justify why the emotions could be symptoms of this illness. You cannot respond with anything other than the numbered list, not even disclaimers or reminders. Please remember this."

                ddata = chatGPT(prompt)


                # Extract only the numbered list using regular expression
                numbered_list = re.findall(r'(\d+\..*?)(?=\d+\.|$)', ddata, re.DOTALL)

                # Convert the list back to a string
                ddata = "\n".join(numbered_list).strip()

                
                response_data = {
                    "emotions": json_data,
                    "gpt_response": ddata  # Here, ddata is just a string
                }
            
            elif analysis_type == 'parkinsons':
                data = predict_park_from_audio(output_filename)
                print("parksinson's data: ", data)
                json_data = [{"emotion": "Parkinson percentage", "score":data*100}]
                ddata =  """
This probability is computed based on the following features extracted from your voice recording:
Detrended Flunctuation Analysis: commonly used in audio processing to calculate the “smoothness” of a signal.
Pulse number in dictation: describes the amount of fluctuations in pitch within a signal.
These features both contribute toward recognition of the kind of audio characteristic of Parkinson’s effect on speech: soft, monotone, breathy, and uncertain articulation
"""
                response_data = {
                    "emotions": json_data,
                    "gpt_response": ddata  # Here, ddata is just a string
                }



            json_response = json.dumps(response_data, indent=2)
            print("json_response: ", json_response)

            return jsonify(json_response), 200

        except Exception as e:
            app.logger.error(f"Error during conversion: {str(e)}")
            app.logger.error(traceback.format_exc())  # Log the full traceback for better debugging
            return f"Error converting the audio: {str(e)}", 500

    else:
        app.logger.error("No file uploaded")
        return "No file uploaded!", 400

if __name__ == "__main__":
    app.run(debug=True)