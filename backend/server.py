from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import datetime
import traceback


app = Flask(__name__)

@app.route("/voiceanalysis")
def voiceanalysis():
    return [{"sad":"22%"}, {"happy":"50%"}]



UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/audio'
ALLOWED_EXTENSIONS = {'ogg', 'mp3', 'wav', 'm4a'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from pydub import AudioSegment

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

        try:
            # Determine the audio format from the file extension and then load using pydub
            extension = file.filename.rsplit('.', 1)[1].lower()
            if extension == "ogg":
                audio = AudioSegment.from_ogg(temp_filename)
            elif extension == "mp3":
                audio = AudioSegment.from_mp3(temp_filename)
            elif extension == "wav":
                audio = AudioSegment.from_wav(temp_filename)
            elif extension == "m4a":
                audio = AudioSegment.from_file(temp_filename, format="m4a")
            else:
                raise ValueError("Unsupported audio format")

            audio.export(output_filename, format="wav")

            # Clean up the temporary file
            os.remove(temp_filename)

            return jsonify({"message": f"File uploaded and converted successfully as {output_filename}!"}), 200

        except Exception as e:
            app.logger.error(f"Error during conversion: {str(e)}")
            app.logger.error(traceback.format_exc())  # Log the full traceback for better debugging
            return f"Error converting the audio: {str(e)}", 500

    else:
        app.logger.error("No file uploaded")
        return "No file uploaded!", 400

if __name__ == "__main__":
    app.run(debug=True)