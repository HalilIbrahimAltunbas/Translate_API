{# @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# def gateway(path):
#     # Gelen isteklerin tüm bilgilerini alıyoruz
#     method = request.method
#     headers = {key: value for key, value in request.headers}
#     data = request.get_data()

#     # Yönlendirilen URL
#     url = f"{TARGET_API_URL}/{path}"
#     print(url)

#     # Yönlendirme işlemi
#     response = None
#     if method == 'GET':
#         response = requests.get(url, headers=headers, data=data)
#     elif method == 'POST':
#         response = requests.post(url, headers=headers, data=data)
#     elif method == 'PUT':
#         response = requests.put(url, headers=headers, data=data)
#     elif method == 'DELETE':
#         response = requests.delete(url, headers=headers, data=data)

#     # Hedef servisten gelen cevabı döndürüyoruz
#     return (response.text, response.status_code, response.headers.items())
}

from flask import Flask, request, jsonify
import requests
from Authentication.utils import auth_required
app = Flask(__name__)

# Hedef API'lerin URL'leri
AUTH_API_URL = "http://localhost:5004"
Translate_Text_URL = "http://localhost:5001"
Speech_Recognition_URL = "http://localhost:5003"
quiz_app_Url = "http://localhost:5005"
OCR_app_Url ="http://localhost:5006"
Gemini_app_URL ="http://localhost:5007"
# Authentication işlemi
def authenticate():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "No token provided"}), 401
    
    # Authentication API'sine istek atıyoruz
    response = requests.post(AUTH_API_URL, headers={'Authorization': token})
    
    if response.status_code != 200:
        return jsonify({"error": "Authentication failed"}), 401
    
    return response.json()

# A operasyonuna yönlendirme
@app.route('/translate-text', methods=['POST'])
@auth_required
def operation_a():
    # Authentication işlemi
    # auth_response = authenticate()
    # if auth_response.get('error'):
    #     return auth_response
    
    # A operasyon API'sine yönlendirme
    response = requests.post(Translate_Text_URL+'/', json=request.json,headers=request.headers)
    return (response.text, response.status_code, response.headers.items())

# B operasyonuna yönlendirme
@app.route('/voice', methods=['POST'])
@auth_required
def operation_b():
    # Authentication işlemi
    # auth_response = authenticate()
    # if auth_response.get('error'):
    #     return auth_response

    headers = dict(request.headers)
    headers.pop('Content-Type')
    
    # B operasyon API'sine yönlendirme
    response = requests.post(Speech_Recognition_URL+'//detect-text-from-voice',
                              files=request.files,
                              headers=headers,
                              )
    return (response.text, response.status_code, response.headers.items())

@app.route('/register/<path:path>', methods=['GET','POST'])

def operation_register(path):
    
    print(path)
    # Authentication işlemi
    # auth_response = authenticate()
    # if auth_response.get('error'):
    #     return auth_response

    
    if request.method == 'POST':    
        # headers = dict(request.headers)
        # headers.pop('Content-Type')
    
    # B operasyon API'sine yönlendirme
        
        response = requests.post(AUTH_API_URL+'/'+path,
                                data = request.get_data(),
                                headers=request.headers,
                                json= request.get_json()
                                )
    elif request.method == 'GET':

        response = requests.get(AUTH_API_URL+'/'+path,
                                data = request.data,
                                headers=request.headers,
                                )
    return (response.text, response.status_code, response.headers.items())

@app.route('/quiz/<path:path>',methods=['GET'])
@auth_required
def get_quiz(path):
    response = requests.get(f"{quiz_app_Url}/{path}",
                data = request.data,
                headers=request.headers
                )
    return (response.text, response.status_code, response.headers.items())

@app.route("/detect-text",methods=['POST'])
def detect_text_from_image():
    headers = dict(request.headers)
    headers.pop('Content-Type')
    
    # B operasyon API'sine yönlendirme
    response = requests.post(OCR_app_Url+'/detect-text',
                              files=request.files,
                              headers=headers,
                              )
    return (response.text, response.status_code, response.headers.items())

@app.route("/gemini",methods = ['POST'])
def ask_gemini():
    print('allright')
    response = requests.post(
                            Gemini_app_URL+'/',
                            headers=request.headers,
                            json=request.json
                            )
    print(response.json())
    return (response.text,response.status_code,response.headers.items())

if __name__ == '__main__':
    # app.run(port=5000)  # Gateway, 5000 portunda çalışacak
    app.run(host='0.0.0.0', port=5000)

