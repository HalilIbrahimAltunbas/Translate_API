from functools import wraps

from flask import make_response, request, current_app,jsonify,Flask

import requests
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-replace-this-in-production'

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if "Bearer" in auth_header else auth_header
            
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # conn = get_db()
            u_id = data['user_id']
            user = requests.get(f'http://127.0.0.1:5002/api/users/{u_id}')
            # user = conn.execute('SELECT * FROM users WHERE id = ?', (data['user_id'],)).fetchone()
            # conn.close()
            
            if not user:
                return jsonify({'message': 'User not found!'}), 401
                
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401
            
        return f(*args, **kwargs)
        
    return decorated


# def auth_required(f):
#     @wraps(f)
#     def decorated(*args,**kwargs):
        
        
#         auth= request.authorization
#         # data = jsonify({"username":auth.username})
#         users = requests.get(f'http://127.0.0.1:5002/api/user/search?{auth.username}')
#         user = users.json()[0]
#         if auth and auth.username == user['username'] and auth.password == user['password']:
#             return f(*args,**kwargs)
#         return make_response('',401,{''})
    
#     return decorated
