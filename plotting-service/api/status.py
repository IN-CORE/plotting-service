from flask import jsonify, make_response

def search():
    message = {
        'status': 'okay',
    }
    resp = jsonify(message)
    resp.status_code = 200

    return make_response(resp)
