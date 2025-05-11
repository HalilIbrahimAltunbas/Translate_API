from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='tr')
app = Flask(__name__)

@app.route('/', methods=['POST'])
def trans_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    # Resmi al ve OCR uygula
    
    
    
    try:
        detected_text = data['text']
        translated =  translator.translate(text=detected_text)
        return jsonify({"text": translated})
    except Exception as e:
        print(f"olmadi {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    # app.run(port=5001) 
    app.run(host='0.0.0.0', port=5001)