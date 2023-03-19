from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.get('/api/poll-user')
def complete_poll():
    token = request.args.get("token")
    if token == None:
        return "You are not logged in. You must sign in to participate in this poll."
    username = request.args.get("username")
    poll_id = request.args.get("pollId")
    response = []
    keys = ["responseOption"]
    result = run_statement("CALL get_user_poll(?)", [poll_id])
    if (type(result) == list):
        current_poll = {}
        for option in result:
            current_poll["question"] = option[4]
            current_poll["questionId"] = option[5]

            current_poll["pollId"] = option[0]

            current_poll["responseId"] = [
                option[6],
            ]
            if response != [] and option[5] == response[-1]["questionId"]:
                response[-1]["responseId"].append(option[6])

            else:
                response.append(current_poll)
                current_poll = {}
        return make_response(jsonify(response), 200)
    

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