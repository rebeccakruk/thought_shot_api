from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement, run_many
from itertools import product
import bcrypt
import json
import uuid


@app.get('/api/poll-response-user')
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
    choices = request.json.get("pollSubmission")
    choice_id = "answerId"
    question_id = "questionId"
    respondent_id = "userId"
    print(type(choices))
    valueWs = []
    val = [()]
    tups = []
    data = json.loads(choices)
    for i in data:
        if isinstance(i, dict):
            for key, value in i.items():
                if 2 >= len(valueWs):
                    valueWs.append(value)
                elif 2 < len(valueWs):
                    val = tuple(valueWs)
                    valueWs = []
                    valueWs.append(value)
                    tups.insert(0,val)
    else:
        val = [()]
        val = tuple(valueWs)
        tups.insert(0,val)
        valueWs = []
    print(tups)
    result = run_many("""INSERT INTO poll_responses(choice_id, question_id, respondent_id) VALUES (%s, %s, %s)""", tups)
    print(result)


