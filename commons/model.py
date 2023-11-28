from google.cloud import datastore
import os
import uuid 
from datetime import datetime

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./test.json"
datastore_client = datastore.Client()

def fetch_user_by_username(username):
    query = datastore_client.query(kind='User')   
    query.add_filter("username", "=", username)  
    user = query.fetch()
    
    return user

def fetch_user_by_email(email):
    print(email)
    query = datastore_client.query(kind='User')   
    query.add_filter("email", "=", email)  
    user = query.fetch()
    
    return user

def fetch_all_user():
    query = datastore_client.query(kind='User')   
    user = query.fetch()

    return user

def create_user(claims, username,fullname):
    print(claims['email'])
    entity_key = datastore_client.key('User', claims['email'])
    entity = datastore.Entity(key = entity_key)
    entity.update({
        'email': claims['email'],
        'full_name': fullname,
        'username':username,
        'profile':"",
        'followers':[],
        'following':[],
        'tweets':[]
    })
    datastore_client.put(entity)
    return entity

def get_profile(email):
    user = fetch_user_by_email(email)
    context = {}
    for i in user:
        full_name=i['full_name']
        username=i['username']
        email = i["email"]
        profile = i["profile"]
        followers = len(i["followers"])
        following = len(i["following"])
        tweets = i['tweets']

        ini_list = add_user_in_tweets(i)
                    
        print ("initial list : ", str(ini_list))
        
        ini_list.sort(key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S.%f'))
        ini_list=ini_list[::-1][:50]

        context = {
        "full_name":full_name,
        "username":username,
        "email":email,
        "profile":profile,
        "tweets":ini_list,
        "followers":followers,
        "following":following
        }
        print(context)
    return context

def add_user_in_tweets(user):
    name = user['full_name']
    username = user['username']
    tweets = []
    for i in user['tweets']:
        i['full_name']=name
        i['username']=username
        tweets.append(i)
    return tweets

def get_following_users_entity(email):
    user = fetch_user_by_email(email)
    following_entities = []
    user_entity= None
    for i in user:
        following = i['following']
        user_entity = i
        for username in following:
            for following_entity in fetch_user_by_username(username):
                following_entities.append(following_entity)
    return {"user":user_entity,"following_entities":following_entities}


def get_following_tweets(email):
    tweets = get_following_users_entity(email)
    timeline_tweets = []
    
    timeline_tweets+=(add_user_in_tweets(tweets['user']))
    if len(tweets['following_entities'])>0:
        for following in tweets['following_entities']:
            timeline_tweets+=(add_user_in_tweets(following))        
    timeline_tweets.sort(key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S.%f'))
    return(timeline_tweets[::-1][:50])

def update_profile_name(email,full_name,profile,):
    entity_key = datastore_client.key('User',email)
    entity=datastore_client.get(entity_key)
    entity.update({
        'full_name': full_name,
        'profile': profile
    })
    datastore_client.put(entity)
    return entity 

def add_tweet(tweet, user):
    entity_key = datastore_client.key('User', user)
    entity = datastore_client.get(entity_key)

    tweets = entity["tweets"]

    tweet_entity_key = datastore_client.key('User')
    tweet_entity = datastore.Entity(key = tweet_entity_key)
    tweet_entity.update(
        {
            'id': str(uuid.uuid4()),
            'desc': tweet['desc'],
            'date': str(datetime.now()),
            'media': tweet['media']
        }
    )

    tweets.append(tweet_entity)

    entity.update(
        {
            'tweets': tweets
        }
    )

    datastore_client.put(entity)

    return "success"

def delete_tweet(email,id):
    tweets = []
    user = fetch_user_by_email(email)
    for prop in user:
        print(prop)
        tweets = prop['tweets']
        for i in tweets:
            if i['id'] == id:
                tweets.remove(i)
                break
        prop.update({
            'tweets':tweets
        })
        datastore_client.put(prop)
    return tweets
  

def update_tweet(email,tweet):
    tweets = []
    user = fetch_user_by_email(email)
    for prop in user:
        print(prop)
        tweets = prop['tweets']
        for i in tweets:
            if i['id'] == tweet['id']:
                
                updated_tweet = tweets.pop(tweets.index(i))
                updated_tweet['desc']=tweet['desc']
                if tweet['media']!='':
                    updated_tweet['media']=tweet['media']
                tweets.append(updated_tweet)
                
                break
        prop.update({
            'tweets':tweets
        })
        datastore_client.put(prop)
    return tweets

def add_follower_following(email,username):
    user = fetch_user_by_email(email)
    second_user = fetch_user_by_username(username)
    follower= []
    following = []
    first_user_username = None
    second_user_email = None

    if user and second_user:
        for i in user:
            following = i['following']
            first_user_username=i['username']
            if not username in following:
                following.append(username)

        for j in second_user:
            follower = j['followers']
            second_user_email = j['email']
            if not first_user_username in follower:

                follower.append(first_user_username)
        
        entity_key = datastore_client.key('User',email )
        entity = datastore_client.get(entity_key)
        print(following)
        # entity['following']=following
        entity.update({
        'following':following

        })
        datastore_client.put(entity)
        entity_key = datastore_client.key('User',second_user_email )
        entity = datastore_client.get(entity_key)
        print(follower)
        # entity['followers']=follower

        entity.update({
        'followers':follower

        })
        print(entity)
        datastore_client.put(entity)
        return "success"
    else:
        return "failure"

def remove_follower_following(email,username):
    user = fetch_user_by_email(email)
    second_user = fetch_user_by_username(username)
    second_user_email=None
    first_user_username = None
    follower= []
    following = []    
    if user and second_user:
        for i in user:
            following = i['following']
            first_user_username=i['username']
            if username in following:

                following.remove(username)


        for j in second_user:
            follower = j['followers']
            second_user_email = j['email']
            if first_user_username in follower:
                follower.remove(first_user_username)
    
        entity_key = datastore_client.key('User',email )
        entity = datastore_client.get(entity_key)
        entity.update({
        'following':following

        })
        datastore_client.put(entity)

        entity_key = datastore_client.key('User',second_user_email )
        entity = datastore_client.get(entity_key)
        entity.update({
        'followers':follower

        })
        datastore_client.put(entity)
        return "success"
    else:
        return "failure"

def fetch_tweet(value):
    users = fetch_all_user()
    tweets=[]
    for i in users:
        user_tweets = add_user_in_tweets(i)
        for j in user_tweets:
            if value in j['desc']:
                tweets.append(j)
    return tweets