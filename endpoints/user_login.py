from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/user-login')
def user_login():
    username = request.json.get("username")
    result = run_statement("CALL get_user_id(?)", [username])
    if (result == []):
        return "Please enter a valid username or register as a new user."
    if (type(result) == list):
        password = result[0][1]
        user_id = result[0][0]
    pw1 = password.encode('utf-8')
    password2 = request.json.get("password")
    if (bcrypt.checkpw(password2.encode(), pw1)):
        token = uuid.uuid4().hex
        results = run_statement("CALL user_login(?, ?)", [token, user_id])
        if results [0][0] == 1:
            response = {
                "userId": user_id,
                "token" : token
                }
            return make_response(jsonify(response), 200)
    else:
        return "Please provide a valid password."