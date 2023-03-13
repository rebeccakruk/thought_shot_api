from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/poll')
def create_poll():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    title = request.json.get("title")
    category = request.json.get("category")
    expiry = request.json.get("expiry")
    invite = request.json.get("inviteOnly")
    limits = request.json.get("limits")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    poll_owner_cert = request.json.get("pollOwnerCert")
    if (type(result) == list):
        owner_id = result[0][0]
        result = run_statement("CALL create_poll(?, ?, ?, ?, ?, ?, ?)", [owner_id, title, category, expiry, invite, limits, poll_owner_cert])
        if (type(result) == list):
            poll_id = result[0][2]
            return f"You've created a new poll, {title}, id: {poll_id}."
        elif "Duplicate entry" in result:
            return f"{title} is already taken. Please choose a new name for your poll."
        else:
            return "Something went wrong, please try again."
            

@app.post('/api/poll/questions')
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
            question_id = result[0][0]
            return f"You've added: '{question}' to the poll. Id: {question_id}."
        print(result)

        result = run_statement("CALL create_choices")

@app.get('/api/poll')
def get_polls():
    token = request.args.get("token")
    username = request.args.get("username")
    user_id = request.args.get("userId")
    response = []
    keys = ["pollId", "title", "description", "category", "pollOwner", "expiry", "createdAt"]
    if token == None:
        result = run_statement("CALL get_all_polls(?)", [user_id])
        if (type(result) == list):
            for poll in result:
                response.append(dict(zip(keys, poll)))
            return make_response(jsonify(response), 200)
    if token != None:
        result = run_statement("CALL get_user_id(?, ?)", [username, token])
        if (type(result) == list):
            owner_id = result[0][0]
            result = run_statement("CALL get_polls_by_owner(?)", [owner_id])
            if result == []:
                result = run_statement("CALL get_all_polls(?)", [user_id])
                if (type(result) == list):
                    for poll in result:
                        response.append(dict(zip(keys, poll)))
                    return make_response(jsonify(response), 200)
            elif (type(result) == list):
                for polls in result:
                    response.append(dict(zip(keys, polls)))
                return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)