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
            current_option["question"] = option[1]
            current_option["responseOption"] = option[3]
            current_option["questionId"] = option[0]
            current_option["responseId"] = [
                option[2]
            ]
            current_option["responseOption"] = [
                option[3]
            ]
            if response != [] and option[0] == response[-1]["questionId"]:
                response[-1]["responseId"].append(option[2])
                response[-1]["responseOption"].append(option[3])
            else:
                response.append(current_option)
                current_option = {}
        return make_response(jsonify(response), 200)
    
                


        #     print("the dictionary 1 is : " + str(response))
        # return make_response(jsonify(response), 200)
    # result = run_statement("CALL get_a(?)", [poll_id])
    # if (type(result) == list):
    #         for info in result:
    #             response_data.append(dict(zip(keys, info)))
    #             print("the dictionary 2 is : " + str(response_data))
    # for (k1, v1), (k2, v2) in zip(response.items(), response_data.items()):
    #     print(k1, '->', v1)
    #     print(k2, '->', v2)           
    #             for idx in range(len(keys1)):
    #                 res[keys1[idx]] = vals2[idx]


        

@app.get('/api/poll-fuser')
def complete_poll():
    token = request.args.get("token")
    if token == None:
        return "You are not logged in. You must sign in to participate in this poll."
    username = request.args.get("username")
    poll_id = request.args.get("pollId")
    response = []
    keys = ["questionId", "responseId"]
    result = run_statement("CALL get_q_and_a(?)", [poll_id])
    if (type(result) == list):
        for option in result:
            response.append(dict(zip(keys, option)))
        return make_response(jsonify(response), 200)

    # if (type(result) == list):
    #         for choice in result:
    #         response.append(dict(zip(keys, choice)))

            

    #     return make_response(jsonify(response, values), 200)
    

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