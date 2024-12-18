from flask import Flask, request, jsonify
import speech_recognition as sr
import io

app = Flask(__name__)

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Read the file into memory
    audio_data = audio_file.read()
    print(f"Received audio file, size: {len(audio_data)} bytes")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Convert audio data into an AudioData object
    try:
        with io.BytesIO(audio_data) as audio_source:
            with sr.AudioFile(audio_source) as source:
                audio_data = recognizer.record(source)

        # Convert speech to text using Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'error': 'Speech recognition could not understand the audio'}), 400
        except sr.RequestError as e:
            return jsonify({'error': f"Could not request results from Google Speech Recognition service; {e}"}), 500
    except Exception as e:
        return jsonify({'error': f"Error processing audio: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
