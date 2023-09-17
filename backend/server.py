from huggingface import predict_emotion_from_audio
from flask import Flask, request, jsonify
from pydub import AudioSegment
import datetime
import os
import json
import traceback

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
            
            data = predict_emotion_from_audio(output_filename)
            # No need to swap or convert anything here

            json_data = [{'emotion': item['label'], 'score': item['score']} for item in data]
            json_string = json.dumps(json_data, indent=2)


            return jsonify(json_string), 200

        except Exception as e:
            app.logger.error(f"Error during conversion: {str(e)}")
            app.logger.error(traceback.format_exc())  # Log the full traceback for better debugging
            return f"Error converting the audio: {str(e)}", 500

    else:
        app.logger.error("No file uploaded")
        return "No file uploaded!", 400

if __name__ == "__main__":
    app.run(debug=True)