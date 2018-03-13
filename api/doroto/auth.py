from flask import jsonify, g, current_app
from flask.ext.httpauth import HTTPBasicAuth
from .models import User

auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    g.user = User.query.filter_by(email=email).first()
    if g.user is None:
        return False
    return g.user.verify_password(password)

@auth.error_handler
def unauthorized():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please authenticate'})
    response.status_code = 401
    return response

@auth_token.verify_password
def verify_auth_token(token, unused):
    print("DATA HERE..............")
    if current_app.config.get('IGNORE_AUTH') is True:
        print("DATA HERE")
        g.user = User.query.get(1)
    else:
        print("DATA HERE THERE")
        g.user = User.verify_auth_token(token)
    return g.user is not None

@auth_token.error_handler
def unauthorized_token():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response
