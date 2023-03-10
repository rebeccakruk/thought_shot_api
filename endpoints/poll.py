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
    if (type(result) == list):
        owner_id = result[0][0]
        result = run_statement("CALL create_poll(?, ?, ?, ?, ?, ?)", [owner_id, title, category, expiry, invite, limits])
        print(result)

@app.post('/api/poll/questions')
def add_questions():
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
    if (type(result) == list):
        owner_id = result[0][0]
        result = run_statement("CALL create_poll(?, ?, ?, ?, ?, ?)", [owner_id, title, category, expiry, invite, limits])
        print(result)
