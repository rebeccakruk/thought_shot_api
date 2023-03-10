from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/user-login')
def user_login():
    username = request.json.get("username")
    password2 = request.json.get("password")
    token = request.json.get("token")
    if token == None:
        result = run_statement("CALL get_user_id(?, ?)", [username, token])
        if (result == []):
            return "Please enter a valid username or register as a new user."
        if (type(result) == list):
            password = result[0][1]
            user_id = result[0][0]
            pw1 = password.encode('utf-8')
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

@app.delete('/api/user-login')
def user_logout():
    token = request.json.get("token")
    if token == None:
        return "You are already signed out."
    result = run_statement("CALL logout_get_session_id(?)", [token])
    if result == []:
        return "You are already signed out."
    if (type(result) == list):
        session_id = result[0][0]
        result = run_statement("CALL user_logout(?)", [session_id])
        if len(result) == 1:
            return "You have successfully logged out."
    else:
        return "Please try again."