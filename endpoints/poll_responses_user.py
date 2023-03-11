from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/poll-response-user')
def user_response():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    response_input = request.json.get("responseOption")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    if (type(result) == list):
        respondent_id = result[0][0]
        result = run_statement("CALL get_choice_id(?)", [response_input])
        if (type(result) == list):
            choice_id = result[0][0]
            result = run_statement("CALL user_response(?, ?)", [respondent_id, choice_id])
        if (type(result) == list):
            return f"{response_input} selected."
        print(result)