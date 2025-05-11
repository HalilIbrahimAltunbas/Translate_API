from flask import Flask, request, jsonify
# import sqlite3
# import os
import jwt
import datetime
import bcrypt
from functools import wraps
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-replace-this-in-production'
app.config['DATABASE'] = 'users.db'
app.config['GOOGLE_CLIENT_ID'] = 'your-google-client-id.apps.googleusercontent.com'  # Replace with your Google Client ID

# Database initialization
# def init_db():
#     if not os.path.exists(app.config['DATABASE']):
#         conn = sqlite3.connect(app.config['DATABASE'])
#         cursor = conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 email TEXT UNIQUE NOT NULL,
#                 password TEXT,
#                 google_id TEXT,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         conn.commit()
#         conn.close()

# init_db()

# Helper function to get database connection
# def get_db():
#     conn = sqlite3.connect(app.config['DATABASE'])
#     conn.row_factory = sqlite3.Row
#     return conn

# JWT token required decorator
def token_required(f):
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

# User registration endpoint
@app.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'All fields are required!'}), 400
        
    # Check if email already exists
    # conn = get_db()
    u_mail = data['email']
    user = requests.get(f'http://127.0.0.1:5002/api/users/mailsearch?email={u_mail}').json()
    # user = conn.execute('SELECT * FROM users WHERE email = ?', (data['email'],)).fetchone()
    
    if user:
        # conn.close()
        return jsonify({'message': 'Email already registered!'}), 409
    
    # Hash the password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Create new user
    res = requests.post('http://127.0.0.1:5002/api/users',
                  json={
                      "username":data['username'],
                      "email":data['email'],
                      "password":str(hashed_password)})
    # cursor = conn.cursor()
    # cursor.execute(
    #     'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
    #     (data['username'], data['email'], hashed_password)
    # )
    # conn.commit()
    # conn.close()
    if res.ok:
        return jsonify({'message': 'User registered successfully!'}), 201
    else: 
        return res.json()

# User login endpoint
@app.route('/auth/signin', methods=['POST'])
def signin():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required!'}), 400
    
    # conn = get_db()
    
    u_mail =data['email']
    user = requests.get(f'http://127.0.0.1:5002/api/users/mailsearch?email={u_mail}')
    # user = conn.execute('SELECT * FROM users WHERE email = ?', (data['email'],)).fetchone()
    print(user)
    if user :
        user = user.json()[0]
    else:
        # conn.close()
        return jsonify({'message': 'Invalid email or password!'}), 401
    
    if user['password']is None:
        # conn.close()
        return jsonify({'message': 'This account uses Google authentication. Please sign in with Google.'}), 401
    
    # Verify password
    # print(bytes(user['password'],'utf-8'))
    print(data['password'].encode('utf-8'))

    # print(bytes(user['password'].lstrip('b').strip("'")))
    if bcrypt.checkpw(data['password'].encode('utf-8'),bytes(user['password'].lstrip('b').strip("'"),'utf-8')):
        # Generate JWT token
        
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        # conn.close()
        return jsonify({
            'message': 'Login successful!',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200
    
    # conn.close()
    return jsonify({'message': 'Invalid email or password!'}), 401

# Google authentication endpoint
@app.route('/auth/google', methods=['POST'])
def google_auth():
    data = request.get_json()
    
    if not data or not data.get('id_token'):
        return jsonify({'message': 'ID token is required!'}), 400
    
    try:
        # Verify Google token
        idinfo = id_token.verify_oauth2_token(
            data['id_token'], 
            google_requests.Request(), 
            app.config['GOOGLE_CLIENT_ID']
        )
        
        # Get user info from token
        google_id = idinfo['sub']
        email = idinfo['email']
        username = idinfo.get('username', '')
        
        # conn = get_db()
        u_mail=data['email']
        user = requests.get(f'http://127.0.0.1:5002/api/users/mailsearch?{u_mail}').json()
        # user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if not user:
            # Create new user with Google info
            response = requests.post('http://127.0.0.1:5002/api/users',
                  json= {
                      'username':data['username'],
                      'email':data['email'],
                      'google_id':google_id})
            # cursor = conn.cursor()
            # cursor.execute(
            #     'INSERT INTO users (username, email, google_id) VALUES (?, ?, ?)',
            #     (username, email, google_id)
            # )
            # conn.commit()
            user_id = response.json().id
        else:
            user_id = user['id']
            
            # Update Google ID if not set
            if not user['google_id']:
                # cursor = conn.cursor()
                # cursor.execute(
                #     'UPDATE users SET google_id = ? WHERE id = ?',
                #     (google_id, user_id)
                # )
                # conn.commit()
                
                requests.put(url=f'http://127.0.0.1:5002/api/users/{user_id}',json={"google_id":google_id})
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        # conn.close()
        return jsonify({
            'message': 'Google authentication successful!',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }), 200
        
    except ValueError as e:
        # Invalid token
        return jsonify({'message': 'Invalid token!', 'error': str(e)}), 401

# Password reset request endpoint
@app.route('/auth/reset-password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required!'}), 400
    
    # conn = get_db()
    # user = conn.execute('SELECT * FROM users WHERE email = ?', (data['email'],)).fetchone()
    # conn.close()
    u_mail =data['email']
    user = requests.get(f'http://127.0.0.1:5002/api/users/mailsearch?{u_mail}')
    if not user:
        # Don't reveal if email exists or not (security feature)
        return jsonify({'message': 'If your email exists in our system, you will receive a password reset link shortly.'}), 200
    
    # Here you would typically:
    # 1. Generate a password reset token
    # 2. Store it in the database with an expiration time
    # 3. Send an email with a link to reset password
    
    # For this example, we'll just return a success message
    return jsonify({'message': 'If your email exists in our system, you will receive a password reset link shortly.'}), 200

@app.route('/auth/is_token_valid',methods=['GET'])
def is_token_valid():
    pass

# Example protected route
@app.route('/user/profile', methods=['GET'])
@token_required
def get_user_profile():
    print(request.headers['Authorization'].split(" "))
    token = request.headers['Authorization'].split(" ")[1] if "Bearer" in request.headers['Authorization'] else request.headers['Authorization']
    print(token)
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    print(data)
    u_id =data['user_id']
    user = requests.get(f'http://127.0.0.1:5002/api/users/{u_id}').json()
    # conn = get_db()
    # user = conn.execute('SELECT id, username, email, created_at FROM users WHERE id = ?', (data['user_id'],)).fetchone()
    # conn.close()
    
    return jsonify({
        "id": user['id'],
        "username": user['username'],
        "email": user['email'],
        "created_at": user['created_at']
    }), 200

if __name__ == '__main__':
    # app.run(debug=True, port=5004)# host='0.0.0.0',
    app.run(host='0.0.0.0', port=5004)