from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/poll-owner')
def create_poll():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    title = request.json.get("title")
    description = request.json.get("description")
    category = request.json.get("category")
    expiry = request.json.get("expiry")
    invite = request.json.get("inviteOnly")
    limits = request.json.get("limits")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    # poll_owner_cert = request.json.get("pollOwnerCert")
    if (type(result) == list):
        owner_id = result[0][0]
        result = run_statement("CALL create_poll(?, ?, ?, ?, ?, ?, ?)", [owner_id, title, description, category, expiry, invite, limits])
        if (type(result) == list):
            response = {
                    "title" : title,
                    "category" : category,
                    "pollId" : result[0][2]
                }
            return make_response(jsonify(response), 200)
        elif "Duplicate entry" in result:
            return f"{title} is already taken. Please choose a new name for your poll."
        else:
            return "Something went wrong, please try again."


@app.post('/api/poll-questions')
def add_questions():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    poll_id = request.json.get("pollId")
    question = request.json.get("question")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    if (type(result) == list):
        result = run_statement("CALL create_question(?, ?)", [poll_id, question])
        if (type(result) == list):
            response = {
                    "question" : question,
                    "pollId" : poll_id,
                    "questionId" : result[0][0]
                }
            return make_response(jsonify(response), 200)
        # if (type(result) == list):
        #     question_id = result[0][0]
        #     return f"You've added: '{question}' to the poll. Id: {question_id}."
        print(result)

        # result = run_statement("CALL create_choices")
@app.get('/api/poll-public')
def get_public_polls():
    response = []
    keys = ["pollId", "title", "description", "categoryName", "pollOwner", "expiry", "createdAt", "category"]
    user_id = request.args.get("userId")
    result = run_statement("CALL get_all_polls(?)", [user_id])
    if (type(result) == list):
        for polls in result:
            response.append(dict(zip(keys, polls)))
        return make_response(jsonify(response), 200)
    else:
        return "Something went wrong, please try again"


@app.get('/api/poll')
def get_polls():
    token = request.args.get("token")
    username = request.args.get("username")
    user_id = request.args.get("userId")
    cat_id = request.args.get("category")
    cat_name = request.args.get("categoryName")
    response = []
    keys = ["pollId", "title", "description", "categoryName", "pollOwner", "expiry", "createdAt", "category"]
    if token != None:
        result = run_statement("CALL get_user_id(?, ?)", [username, token])
        if (type(result) == list):
            owner_id = result[0][0]
            result = run_statement("CALL get_polls_by_owner(?)", [owner_id])
            if result == []:
                result = run_statement("CALL get_all_polls(?)", [user_id])
                if (type(result) == list):
                    current_category = {}
                for poll in result:
                    current_category["pollId"] = poll[0]
                    current_category["title"] = poll[1]
                    current_category["description"] = poll[2]
                    current_category["categoryName"] = poll[3]
                    current_category["pollOwner"] = poll[4]
                    current_category["expiry"] = poll[5]
                    current_category["createdAt"] = poll[6]
                    current_category["category"] = poll[7]
                    if response != [] and poll[0] == response[-1]["pollId"]:
                        response[-1]["category"].append(result)
                    else:
                        response.append(current_category)
                        current_category = {}       
                return make_response(jsonify(response), 200)
                    # for poll in result:
                    #     response.append(dict(zip(keys, poll)))
                    # return make_response(jsonify(response), 200)
            elif (type(result) == list):
                for polls in result:
                    response.append(dict(zip(keys, polls)))
                return f"{username}, {owner_id}" and make_response(jsonify(response), 200)
    if token == None and cat_name == None and cat_id == None:
        result = run_statement("CALL get_all_polls(?)", [user_id])
        if (type(result) == list):
            current_category = {}
            for poll in result:
                current_category["pollId"] = poll[0]
                current_category["title"] = poll[1]
                current_category["description"] = poll[2]
                current_category["categoryName"] = poll[3]
                current_category["pollOwner"] = poll[4]
                current_category["expiry"] = poll[5]
                current_category["createdAt"] = poll[6]
                current_category["category"] = poll[7]
                if response != [] and poll[0] == response[-1]["pollId"]:
                    response[-1]["category"].append(result)
                else:
                    response.append(current_category)
                    current_category = {}       
        return make_response(jsonify(response), 200)
    if token == None and cat_name != None and cat_id == None:
        result = run_statement("CALL get_polls_by_cat(?, ?)", [cat_id, cat_name])
        if (type(result) == list):
            for cat in result:
                response.append(jsonify(response), 200)
            else:
                response.append(jsonify(result), 500)
    if token == None and cat_name == None and cat_id != None:
        result = run_statement("CALL get_polls_by_cat(?, ?)", [cat_id, cat_name])
        if (type(result) == list):
            for cat in result:
                response.append(jsonify(response), 200)
            else:
                response.append(jsonify(result), 500)
    else:
        return make_response(jsonify(response), 500)

@app.get('/api/poll-owner')
def get_my_polls():
    token = request.args.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.args.get("username")
    poll_id = request.args.get("pollId")
    response = []
    keys = ["pollId", "title", "description", "categoryName", "pollOwner", "expiry", "createdAt", "questionId", "responseOption", "answerId"]
    if token != None:
        result = run_statement("CALL get_user_id(?, ?)", [username, token])
        if (type(result) == list):
            owner_id = result[0][0]
            result = run_statement("CALL get_polls_by_owner(?, ?)", [owner_id, poll_id])
            if (type(result) == list):
                for poll in result:
                    response.append(dict(zip(keys, poll)))
            return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(response), 500)

@app.delete('/api/poll-owner')
def delete_poll():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    poll_id = request.json.get("pollId")
    if token != None:
        result = run_statement("CALL get_user_id(?, ?)", [username, token])
        if (type(result) == list):
            result = run_statement("CALL delete_poll(?)", [poll_id])
            if result == None:
                return "You have logged out successfully"
        else:
            return "Something went wrong, please try again."               

    