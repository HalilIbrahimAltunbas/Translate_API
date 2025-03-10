from functools import wraps

from flask import make_response, request, current_app,jsonify
import requests

def auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        
        
        auth= request.authorization
        # data = jsonify({"username":auth.username})
        users = requests.get(f'http://127.0.0.1:5002/api/user/search?{auth.username}')
        user = users.json()[0]
        if auth and auth.username == user['username'] and auth.password == user['password']:
            return f(*args,**kwargs)
        return make_response('',401,{''})
    
    return decorated
