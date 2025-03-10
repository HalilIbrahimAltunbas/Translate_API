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
AUTH_API_URL = "http://localhost:5001/authenticate"
A_API_URL = "http://localhost:5002/operation_a"
B_API_URL = "http://localhost:5003/operation_b"

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
    auth_response = authenticate()
    if auth_response.get('error'):
        return auth_response
    
    # A operasyon API'sine yönlendirme
    response = requests.post(A_API_URL, json=request.json)
    return (response.text, response.status_code, response.headers.items())

# B operasyonuna yönlendirme
@app.route('/operation_b', methods=['POST'])
def operation_b():
    # Authentication işlemi
    auth_response = authenticate()
    if auth_response.get('error'):
        return auth_response
    
    # B operasyon API'sine yönlendirme
    response = requests.post(B_API_URL, json=request.json)
    return (response.text, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(port=5000)  # Gateway, 5000 portunda çalışacak

