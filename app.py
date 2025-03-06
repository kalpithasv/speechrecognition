import os
from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def home():
    return "Speech Recognition API is running!"

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Speech not recognized"}), 400
    except sr.RequestError:
        return jsonify({"error": "API unavailable"}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
