from datetime import datetime, timedelta, timezone
from jose import jwt 
from functools import wraps
from flask import request, jsonify
import jose

SECRET_KEY = "secret key for JSON Web Token"

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1), # sets an expiration for 1 hour
        'iat': datetime.now(timezone.utc),  # time issued at
        'sub': str(customer_id)        
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # looks fo token in Authorization header
        if 'Authorization' in request.headers: 
            token = request.headers['Authorization'].split(" ")[1]
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            customer_id = data['sub']
        
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        
        except jose.exceptions.JWTError:
            return jsonify({'message': 'Invalid Token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated