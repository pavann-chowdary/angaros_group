from flask import *
import pandas as pd
import numpy as np
import re
import tweepy    
import json
import requests


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/twitter")
def twitter():
    #GET KEYS FROM FILE
    ApiKeys=pd.read_csv('TwitterApikeys.csv')
    ConsumerKey=ApiKeys['ApiKey'][0]
    ConsumerSecretKey=ApiKeys['ApiSecretKey'][0]
    #AccessToken=ApiKeys['AccessToken'][0]
    AccessToken='1084115865245646848-CuOVgZcqrTTUwPs0ZHYUboqmas4qmF'
    AccessSecretToken=ApiKeys['AccessSecretToken'][0]
    #CREATE AUTHENTICATION OBJECT
    auth=tweepy.OAuthHandler(ConsumerKey,ConsumerSecretKey)
    #SET ACCESSTOKEN AND ACCESSSECRETTOKEN
    auth.set_access_token(AccessToken,AccessSecretToken)
    #CREATE API OBJECT WHILE PASSING AUTHENTICATION INFORMATION
    api=tweepy.API(auth,wait_on_rate_limit=True)
    #EXTRACT 100 TWEETS FROM TWITTER USER
    tweets=api.user_timeline(screen_name="Angaros_Group",count=100,lang='en',tweet_mode='extended')
    #printing 10 tweets
    c=0
    print('Recent 100 Tweets Of @Angaros_Group')
    data = []
    for tweet in tweets[0:100]:
        c+=1
        new_data = []
        new_data.append(tweet.full_text)
        try:
            if(tweet.id_str[:9]==str(tweet.entities['media'][0]['id'])[:9]):
                new_data.append(tweet.entities['media'][0]['media_url'])
        except:
            new_data.append("No Media")

        data.append(new_data)
    return render_template("twitter.html",data=data)


@app.route("/facebook")
def facebook():
    token='EAACiFj0RLisBAG8yZCQHaXvoz1qZBJB8DU5dqvW8Q5SPuIjYxO0dthRlTu2dOjD0Oy2d2ppz53GtZCCJdq2dhZCWY7ms82qZABIgy9mEGgbRQl7uD6BVu8OayzPoqAAkZCnZCQ2xkkmcSbZC34YkqqkkgXncqxfNNaRBTqympDXfKgZDZD'
    res = requests.get("https://graph.facebook.com/v10.0/495152637273035/photos?access_token="+token+"&fields=images%2Cid&limit=25&after=MzEwODYxMDk3MjU5Mzg0MgZDZD")
    res1 = requests.get("https://graph.facebook.com/v10.0/234723296649305/posts?access_token="+token+"&pretty=0&limit=25&after=QVFIUjFFVVR3Vl9JNDRZAUjRBOTNkMU45VnlUQ1VZAVGp2VWRocjNSWWIwN1NuN3VPMDBFdExCSkdEek0wQk5xVFg2X3dYNElFN3ZAHMUZA3YThnQUduQU11U0p1S014dGhQNjlLQ0ZAyNlJQZAlg2U0w2aVlFejZA2OVJlZATFoRndvMlRSSkNv")
    images_data = []
    posts_data = []
    n=1
    while(n<5):
        after_dat = res.json()['paging']['cursors']['after']
        after_dat_posts = res1.json()['paging']['cursors']['after']
        data = res.json()['data']
        data1 = res1.json()['data']
        for i in data:
            li = []
            li.append(i['images'][0])
            li.append(i['id'])
            images_data.append(li)
        for i in data1:
            post_id = i['id'].split("_")
            post_id = post_id[1]
            posts_data.append(list([i,post_id]))
        res = requests.get("https://graph.facebook.com/v10.0/495152637273035/photos?access_token="+token+"&fields=images%2Cid&limit=25&after="+after_dat)
        res1 = requests.get("https://graph.facebook.com/v10.0/234723296649305/posts?access_token="+token+"&pretty=0&limit=25&after="+after_dat_posts)
        n += 1
        
    final_posts_data = []
    for i in images_data:
        for j in posts_data:
            if(j[1]==i[1]):
                final_posts_data.append(list([i,j]))
    return render_template("facebook.html",data = final_posts_data)



