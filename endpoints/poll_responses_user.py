from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
from itertools import product
import bcrypt
import uuid


@app.get('/api/poll-user')
def get_qa():
    poll_id = request.args.get("pollId")
    keys = ["questionId", "question", "responseId", "responseOption", "pollId", "title", "description"]
    response = []
    result = run_statement("CALL get_q_and_a(?)", [poll_id])
    if (type(result) == list):
        current_option = {}
        for option in result:
            current_option["title"] = option[5]
            current_option["description"] = option[6]
            current_option["question"] = option[1]

            current_option["questionId"] = option[0]
            current_option["answers"] = [
            ]
            if response != [] and option[0] == response[-1]["questionId"]:
                response[-1]["answers"].append({
                    "answerId": option[2],
                    "responseOption" : option[3]
                    }
                    )
            else:
                response.append(current_option)
                current_option = {}
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