from flask import Flask, request, jsonify
import speech_recognition as sr
import requests
from werkzeug.datastructures.headers import Headers
import base64
app = Flask(__name__)

@app.route('/detect-text-from-image', methods=['POST'])
def detect_text_from_image():
    try:
        print('ok')
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        # Resmi al ve OCR uygula
        file = request.files['image']


        b64 = base64.b64encode(file.read()).decode("utf-8")
        url = " https://e1d8-34-53-74-40.ngrok-free.app/ocr"
        res = requests.post(url, json={"image": b64})
        print(res.json())
        # res=["hello","my","name","is","halil"]
        text = " ".join(res.json().get("results"))
        headers = dict(request.headers)
        headers['Content-Type'] = 'application/json'
        translated =  requests.post(url='http://127.0.0.1:5000/translate-text',
                                    json={"text": text},
                                    headers=headers)



        return jsonify({"text":translated.json().get('text')})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.run(port=5003) 
    app.run(host='0.0.0.0', port=5006)