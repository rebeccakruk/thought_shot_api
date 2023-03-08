from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/user')
def user_signup():
    username = request.json.get("username")
    pw = request.json.get("password")
    if pw == None:
        return "You must choose a password to complete signup."
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(pw.encode(), salt)
    email = request.json.get("email")
    dob = request.json.get("dob")
    token = uuid.uuid4().hex
    image = request.json.get("profile image")
    keys = ["userId", "token"]
    response = []
    result = run_statement("CALL user_signup(?, ?, ?, ?, ?, ?)", [username, password, email, dob, token, image])
    if (type(result) == list):
        for data in result:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    if "Duplicate entry" in result:
        return "That username is already taken. Please choose another name."
    else:
        return "Please provide a valid password."

@app.get('/api/user')
def user_get():
    token = request.args.get("token")
    if token == None:
        return "You must login to see your profile info"
    username = request.args.get("username")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    response = []
    keys = ["userId", "email", "username", "image", "createdAt"]
    if (type(result) == list):
        for user in result:
            response.append(dict(zip(keys, user)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)
    
@app.patch('/api/user')
def user_edit():
    token = request.json.get("token")
    if token == None:
        return "You are not logged in. Please login to update your profile."
    username = request.json.get("username")
    password = request.json.get("password")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    print(result)
                