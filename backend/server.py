from flask import Flask

app = Flask(__name__)

@app.route("/voiceanalysis")
def voiceanalysis():
    return {"voice":["sad", "happy", "angry"]}

if __name__ == "__main__":
    app.run(debug=True)