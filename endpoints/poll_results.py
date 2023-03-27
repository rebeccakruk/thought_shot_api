from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.get('/api/poll-results')
def get_results():
    poll_id = request.args.get('pollId')
    result = run_statement("CALL get_results(?)", [poll_id])
    if (type(result) == list):
        print(result)