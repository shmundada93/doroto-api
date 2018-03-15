from flask import jsonify

def unauthorized(message):
    response = jsonify({'error': 'Unauthorized', 'message': "Incorrect role"})
    response.status_code = 403
    return response