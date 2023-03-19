from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/poll-response')
def create_choices():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    question_id = request.json.get("questionId")
    response_input = request.json.get("responseOption")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    if (type(result) == list):
        result = run_statement("CALL create_choices(?, ?)", [question_id, response_input])
        if (type(result) == list):
            response = {
                "responseOption" : response_input,
                "responseId" : result[0][0]
            }
            return make_response(jsonify(response), 200)
        print(result)

        # the owner posts a question (one procedure, and is promted to post the response, one after the next in another procedure. the reponses to to a different table)