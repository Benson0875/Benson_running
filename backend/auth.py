from flask_httpauth import HTTPTokenAuth
import jwt
from functools import wraps
from flask import request, abort, g
import os
from flask import jsonify
import logging

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "app.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

auth = HTTPTokenAuth(scheme='Bearer')

def init_auth(app):
    @auth.verify_token
    def verify_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user = data['user']
            return True
        except:
            return False

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.getenv('API_KEY'):
            abort(401, description="Invalid API key")
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error: {e}, Context: {request.path}")
            return jsonify({'error': str(e)}), 400
    return decorated_function

def format_response(data, status_code=200):
    return jsonify({
        'status': 'success',
        'data': data
    }), status_code 