from flask import Flask, request, jsonify
import speech_recognition as sr
import requests
from werkzeug.datastructures.headers import Headers
app = Flask(__name__)

@app.route('/detect-text-from-voice', methods=['POST'])
def detect_text_from_voice():
    print(request.files)
    if 'file' not in request.files:
        return jsonify({"error": "No voice file provided"}), 400
    
    audio = request.files['file']
    file_path = os.path.join('uploaded_audio', 'audio.3gp')
    recognizer = sr.Recognizer()

    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # # Dosyayı kaydet
    audio.save(file_path)
    convert_to_wav(file_path,file_path)
    
    
    try:
        with sr.AudioFile(file_path.replace('.3gp', '.wav')) as source:
            # print(audio)
            audiofile = recognizer.record(source)
            text = recognizer.recognize_google(audiofile, language="en-US")
            

            headers = dict(request.headers)
            headers['Content-Type'] = 'application/json'
            
            
            
            
            translated =  requests.post(url='http://127.0.0.1:5000/translate-text',json={"text": text},headers= headers)
            return jsonify(translated.json())

    except sr.UnknownValueError:
        return jsonify({"Ses anlaşılamadı."}), 500

    except sr.RequestError as e:
        return jsonify({f"Hata: {e}"}), 500


from pydub import AudioSegment
import os

def convert_to_wav(input_path, output_path):
    try:
        # Dosyayı yükle ve WAV formatına dönüştür
        print(input_path)
        audio = AudioSegment.from_file(input_path)
        print("a")
        audio.export(output_path.replace('.3gp', '.wav'), format="wav")
        print("b")
        return output_path
    except Exception as e:
        raise ValueError(f"Ses dosyası dönüştürülemedi: {e}")
    
if __name__ == '__main__':
    # app.run(port=5003) 
    app.run(host='0.0.0.0', port=5003)