from flask import Flask, request, jsonify
from pytesseract import image_to_string , pytesseract
import cv2 
from PIL import Image
import numpy as np

from deep_translator import GoogleTranslator
translator = GoogleTranslator(source='auto', target='tr')

app = Flask(__name__)

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

@app.route('/detect-text', methods=['POST'])
def detect_text():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Resmi al ve OCR uygula
    file = request.files['image']
    
    try:
        image = Image.open(file)#.convert('RGB')
        # image.save("sended.png")
        # image = np.array(image)
        # print(f"a {image}")
        # image = np.asarray(bytearray(image.read()), dtype="uint8")
        # print(f"b {image}")
        # image = cv2.imdecode(image,cv2.IMREAD_ANYCOLOR)
        # print(f"c {image}") 
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        # print(f"d {image}")
        # image.save("sended.png")
        detected_text = image_to_string(image)
        translated =  translator.translate(text=detected_text)
        return jsonify({"text": translated})
    except Exception as e:
        print(f"olmadi {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # app.run(port=5001) 
    app.run(host='0.0.0.0', port=5006)