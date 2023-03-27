from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.get('/api/poll-results')
def get_results():
    poll_id = request.args.get('pollId')
    response = []
    keys = ["question", "responseOption"]
    result = run_statement("CALL get_results(?)", [poll_id])
    if (type(result) == list):
        for data in result:
            response.append(dict(zip(keys, data)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)


