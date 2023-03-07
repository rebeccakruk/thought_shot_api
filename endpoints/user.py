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
    dob = request.json.get("dob YYYY/MM/DD")
    token = uuid.uuid4().hex
    image = request.json.get("profile image")
    keys = ["userId", "token"]
    response = []
    result = run_statement("CALL user_signup(?, ?, ?, ?, ?, ?)", [username, password, email, dob, token, image])
    if (type(result) == list):
        for data in result:
            response.append(dict(zip(keys, data)))
            return make_response(jsonify(response), 200)
    else:
        return "Please provide a valid password."