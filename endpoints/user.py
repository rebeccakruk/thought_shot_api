from app import app, __init__
from flask import jsonify, make_response, request
from dbhelpers import run_statement
import bcrypt
import uuid

@app.post('/api/user')
def user_signup():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    username = request.json.get("username")
    pw = request.json.get("password")
    if pw == None:
        return "You must choose a password to complete signup."
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(pw.encode(), salt)
    email = request.json.get("email")
    dob = request.json.get("dob")
    token = uuid.uuid4().hex
    result = run_statement("CALL user_signup(?, ?, ?, ?, ?, ?, ?, ?)", [username, password, email, dob, token, first_name, last_name])
    if (type(result) == list):
        user_id = result[0][0]
        token = result[0][1]
        response = {
            "userId": user_id,
            "token": token
        }
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
    keys = ["userId", "email", "username", "firstName", "lastName", "createdAt", "dob", "token"]
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
    email = request.json.get("email")
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    result = run_statement("CALL get_user_id(?, ?)", [username, token])
    if (type(result) == list):
        user_id = result[0][0]
        if last_name != None and email == None and first_name == None:
            result = run_statement("CALL patch_ln(?, ?)", [user_id, last_name])
            if result == None:
                return f"You've successfully updated your last name to {last_name}."
        if last_name != None and email != None and first_name == None:
            result = run_statement("CALL patch_ln_email(?, ?, ?)", [user_id, last_name, email])
            if result == None:
                return "You've successfully updated your info."
        if last_name != None and email == None and first_name != None:
            result = run_statement("CALL patch_fn_ln(?, ?, ?)", [user_id, first_name, last_name])
            if result == None:
                return "You've successfully updated your info."
        if email != None and last_name == None and first_name == None:
            result = run_statement("CALL patch_email(?, ?)", [user_id, email])
            if result == None:
                return "You've successfully updated your info."
        if email != None and last_name == None and first_name != None:
            result = run_statement("CALL patch_email_fn(?, ?, ?)", [user_id, email, first_name])
            if result == None:
                return "You've successfully updated your info."
        if first_name != None and last_name == None and email == None:
            result = run_statement("CALL patch_fn(?, ?)", [user_id, first_name])
            if result == None:
                return "You've successfully updated your info."
        else:
            result = run_statement("CALL patch_all(?, ?, ?, ?)", [user_id, email, last_name, first_name])
            if result == None:
                return "You've successfully updated your info."
            else:
                return "uh oh."
    else:
        return "hmmm."
    
    # the answers have to be in a separate table (FK that points to the question)
    # assume the api is a question and the array of possible answers, object being sent over, a question and a bunch of answers
    # if the wf gets interrupted
    # assuming that the q and i come 
    # then handle the answering polls wf
    # finished teh signup/login wf
    # next is the base of the abaility to create polls, edit polls but probably, you can edit the answers before you publish them
    # which gives the pool to make it live
    # two types of accounts
    # anybody can participate in a poll, creating a poll and launching it
    # the next one is the actual options or a way to view polls
    # invitation by link or whoever and whatever
    # pool categories
    # some with expiry dates 
    # the scenarios with people that use the serve 
    # a real design principal, where you imagine personas that use the serve
    # think of the workflow that you're going t obe polling through
    # is. the next office outing out of a few
    # imagine the system the way that I want it, which is why we limit the definitive advice