import email
import google.oauth2.id_token
from flask import Flask, render_template, request,redirect,url_for
from google.auth.transport import requests
from commons import model
from datetime import datetime

firebase_request_adapter = requests.Request()

def check_data():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)
    return (claims,error_message)

def check_username(username):
    user = model.fetch_user_by_username(username)
    check = None
    for i in user:
        check=i['username']
    if check:
        return "username already exist"
    else:
        return "good"
    
def fetch_username(user):
    for i in user:
        return i['username']

def check_following(email,username):
    user = model.fetch_user_by_email(email)
    for i in user:
        i['following']
        if username in i['following']:
            return True
        else:
            return False

def fetch_all_usernames(value):
    users=model.fetch_all_user()
    usernames = []
    for i in users:
        if value in i['username']:
            usernames.append(i)
    return usernames