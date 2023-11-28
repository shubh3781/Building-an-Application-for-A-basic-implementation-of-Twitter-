import datetime
from flask import Flask, render_template, request,redirect,url_for , flash,jsonify,make_response
from google.cloud import datastore,storage
import google.oauth2.id_token
from google.auth.transport import requests
import json
from werkzeug.utils import secure_filename
import os
from urllib3 import HTTPResponse
from commons import controller,model,constants


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


datastore_client = datastore.Client()

firebase_request_adapter = requests.Request()

def addFile(file):
    storage_client = storage.Client(project=constants.PROJECT_NAME)
    bucket = storage_client.bucket(constants.PROJECT_STORAGE_BUCKET)
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)


@app.route('/signin')
def signin():
    return render_template('index.html')

@app.route('/')
def root():
    data = controller.check_data()
    print(data[0])
    if data[0] != None:
        return redirect('/timeline')
        
    return render_template('index.html', user_data=data[0], error_message=data[1])

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    user_name = None
    show=False
    if request.method == "POST":
        print(request.form['username'])
        user = "@" +str(request.form['username'])
        fullname = str(request.form['fullname'])
        print(user)
        print(fullname)
        return redirect(url_for("usernametimeline", user=user,fullname=fullname))
    
    data = controller.check_data()
    if data:
        
        
        user = model.fetch_user_by_email(data[0]['email'])
      
        if user:
            user_name = controller.fetch_username(user)
            print(user_name)
            tweets=None
            if user_name:
                tweets = model.get_following_tweets(data[0]['email'])
                print(tweets)
                if tweets:
                    show=True
        

            return render_template('timeline.html', user_data=data[0], error_message=data[1],user_name=user_name,tweets=tweets,show=show)
        
        else:
            return render_template('timeline.html', user_data=data[0], error_message=data[1],user_name=user_name,show=show)
            

@app.route('/timeline/<user>/<fullname>')
def usernametimeline(user,fullname):
    msg=None
    user_name = None
    data = controller.check_data()
    if data:
        check = controller.check_username(user)
        print(check)
        if check != "username already exist":
            model.create_user(data[0],user,fullname)
            
            print(user)
            user_name= user
            msg=check
        else:
            msg=user
            
    return render_template('timeline.html', user_data=data[0], error_message=data[1],user_name=user_name,msg=msg)

@app.route('/profile', methods=['GET','POST'])
def profile():
    data = controller.check_data()
    if data:
       
        profile = model.get_profile(data[0]['email'])
        return render_template('profile.html', user_data=data[0], error_message=data[1], profile=profile,edit=True,unfollow=True)

@app.route('/profile/<username>', methods=['GET','POST'])
def others_profile(username):
    unfollow = False
    email=None
    data = controller.check_data()
    following = controller.check_following(data[0]['email'],username)
    user = model.fetch_user_by_username(username)
    sign_in_user =model.fetch_user_by_email(data[0]["email"])
    for i in sign_in_user:
        if i['username'] == username:
            unfollow=True
    for i in user:
        email=i['email']
    if email:        
        profile = model.get_profile(email)
        return render_template('profile.html', user_data=user, profile=profile,edit=False,following=following,unfollow=unfollow)    

@app.route('/addfollower',methods=['POST'] )
def addfollower():
    data = controller.check_data()
    email=data[0]['email']
    payload = request.json
    if payload:
        res_data = model.add_follower_following(email,payload['username'])
        return make_response(jsonify(res_data),200)
    else:
        return make_response(jsonify({'msg':'payload not found'}),400)

@app.route('/removefollower',methods=['POST'] )
def removefollower():
    data = controller.check_data()
    email=data[0]['email']
    
    payload = request.json
    print(payload['username'])
    if payload:
        res_data = model.remove_follower_following(email,payload['username'])
        return make_response(jsonify(res_data),200)
    else:
        return make_response(jsonify({'msg':'payload not found'}),400)

@app.route('/editprofile',methods=['POST'] )
def editprofile():
    data = controller.check_data()
    email=data[0]['email']
    payload = request.json
    if payload:
        res_data = model.update_profile_name(email,payload['full_name'],payload['profile'])
        return make_response(jsonify(res_data),200)
    else:
        return make_response(jsonify({'msg':'payload not found'}),400)

@app.route('/addtweet',methods=['POST'] )
def createtweet():
    data = controller.check_data()
    email=data[0]['email']
    payload = request.form

    print(payload)
    tweet_data = {'desc':request.form['desc'],'media':''}
    if request.files:
        file = request.files['file_name']
        if file.filename != '':
            addFile(file)
            link = "https://storage.cloud.google.com/"+constants.PROJECT_STORAGE_BUCKET+"/"+file.filename
            tweet_data['media']=link
            print('f',tweet_data)
    
    if request.form:
        res_data = model.add_tweet(tweet_data,email)
        
        return redirect('/timeline')
    else:
        return make_response(jsonify({'msg':'payload not found'}),400)

@app.route('/updatetweet',methods=['POST'] )
def updatetweet():
    data = controller.check_data()
    email=data[0]['email']
    payload = request.form
    tweet_data = {'desc':request.form['desc'],'media':'','id':request.form['id']}
    print(tweet_data)
    if request.files:
        file = request.files['media']
        if file.filename != '':
            addFile(file)
            link = "https://storage.cloud.google.com/"+constants.PROJECT_STORAGE_BUCKET+"/"+file.filename
            tweet_data['media']=link
        
    
    if payload:
        res_data = model.update_tweet(email,tweet_data)
        return redirect('/profile')
    else:
        return make_response(jsonify({'msg':'payload not found'}),400)

@app.route('/deletetweet',methods=['POST'] )
def deletetweet():
    data = controller.check_data()
    email=data[0]['email']
    payload = request.json
    if payload:
        res_data = model.delete_tweet(email,payload['id'])
        return make_response(jsonify(res_data),200)
    else:
        return make_response(jsonify({'msg':'payload not found'}),400)

@app.route('/search', methods=['GET', 'POST'])
def search():
    value = request.form['searchfilter']
    tweets=None
    data = controller.check_data()
    users=None
    print(value)
    if '@' in value:
        users = controller.fetch_all_usernames(value)
        print(users)
        if users:
            return render_template('search.html', user_data=data[0], error_message=data[1], tweets= tweets,users=users)

    else:
        tweets = model.fetch_tweet(value)
        print(tweets)
        if tweets:
            return render_template('search.html', user_data=data[0], error_message=data[1], tweets= tweets,users=users)
        
    return redirect('timeline') 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)