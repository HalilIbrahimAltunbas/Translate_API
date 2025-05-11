from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
from google import genai
from google.genai import types

client = genai.Client(api_key="")

translator = GoogleTranslator(source='auto', target='tr')
app = Flask(__name__)

scenarios = {
    1: "Sen bir restoranda garsonsun. Kullanıcıyla sipariş hakkında İngilizce sohbet et.",
    2: "Sen bir oteldeki resepsiyonistsin. Kullanıcıyla rezervasyon hakkında İngilizce konuş.",
    3: "Sen bir havaalanında görevli memursun. Kullanıcı bilet ve uçuş hakkında soru soruyor.",
    4: "Sen bir market kasiyerisinsin. Kasada kullanıcıyla alışveriş konuşması yap.",
    5: "Sen bir doktora gitmiş hastasın. Kullanıcı doktor rolünde, seni muayene etmeye çalışıyor.",
}

stress_test_inputs = {
    1: "Hello! How are you today?",
    2: "Merhaba, bugün nasılsın? Bugün hava çok güzel ve parklarda yürüyüş yapmak harika olurdu değil mi?",
    3: "これは日本語で書かれたテキストです。これはUIがUnicode'u düzgün gösterip göstermediğini test eder。",
    4: "🤖👋🎉🌍💬 – Emojilerle dolu bir test mesajı! Bakalım nasıl görünüyor?",
    5: "1234567890!@#$%^&*()_+-=[]{}|;':\",./<>?`~ ← özel karakterler testi",
    6: "a" * 500,  # 500 karakterlik uzun test mesajı
    7: "lorem ipsum " * 100,  # 1000+ kelimelik bir spam metin
    8: "\n\n\nBu mesajın içinde çok fazla satır boşluğu var.\n\n\nİçeriğin bozulmasına sebep olabilir mi?",
    9: "This is a test to see how the system reacts to extremely rapid sequences of short inputs. Test. Test. Test. Test. Test.",
    10: "🚀 Mixed test: Türkçe, English, 日本語, العربية, Русский, emojis 🤯, special $$$!!! and long length: " + ("XYZ " * 100),
    11: "",  # boş girdi
    12: "      ",  # sadece boşluk
    13: "بِسْمِ ٱللّٰهِ",  # sağdan sola yazılan dil desteği
    14: "🚫❌💥 ERROR SIMULATION: The system crashed while trying to respond to your input. Please contact support.",
    15: "🧠✨ What is the meaning of life, the universe, and everything?",
}


@app.route('/', methods=['POST'])
def trans_text():
    user_msg = request.get_json()
    print(user_msg)
    if not user_msg or not ("role" or "message" in user_msg):
        print('bad json')
        return jsonify({'error': 'bad json'}), 400

    # Resmi al ve OCR uygula
    
    
    
    try:
        # response = client.models.generate_content(
        #     model="gemini-2.0-flash",
        #     config=types.GenerateContentConfig(
        #     system_instruction="You are an English teacher. Have a daily conversation with the user. If the user speaks Turkish, translate to English first, then reply. Also write the Turkish meaning of important words in parentheses."),
        #     contents=user_msg
        # )
        return jsonify({'response': stress_test_inputs.get(int(user_msg["message"]))})
    except Exception as e:
        print(f"olmadi {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    # app.run(port=5001) 
    app.run(host='0.0.0.0', port=5007)