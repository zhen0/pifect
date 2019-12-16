# @author Daniel Egan
# Twitter bot auto-posting content.
# Uses Prefect, GoogleSheets, Twitter, and Pushbullet APIs.
# Use at your own risk.
import os
import pandas as pd
import yaml
from datetime import date, timedelta
# Use google sheets as easy-access database
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Twitter
import twitter
# Prefect
from prefect import task, Flow, Task
from prefect.schedules import IntervalSchedule
# Pushbullet
from pushbullet import Pushbullet

# This is where my credentials are kept,
# except for GSheets which uses a different format.
credentials_file = os.path.join('/', 'Users', 'danielegan', 'src','degan_creds.yaml')
#credentials_file = os.path.join('credentials.yaml')
# Set up the task state handler, to notify me of any issues.
def load_creds(local_yaml_file):
    creds = yaml.safe_load(open(local_yaml_file, 'r'))
    return creds
creds = load_creds(credentials_file)
pb = Pushbullet(creds['pushbullet']['token'])


def sendPushBulletOnFail(task, old_state, new_state):
    if new_state.is_failed():
        msg = "{0} failed in state {1}".format(task, new_state)
        pb.push_note('Flow Error', msg)
    return new_state
t = Task(state_handlers=[sendPushBulletOnFail])

# Flow Components --------------------------
@task(name= "twitter_auth", slug = "twitter_auth", state_handlers=[sendPushBulletOnFail])
def twitterAuth(creds):
    twitter_creds = creds['twitter']
    api = twitter.Api(consumer_key        = twitter_creds['consumer_key'],
                      consumer_secret     = twitter_creds['consumer_secret'],
                      access_token_key    = twitter_creds['access_token'],
                      access_token_secret = twitter_creds['access_token_secret'])
    return api

# Autheticate
@task(name= "gsheets_auth", slug = "gsheets_auth", state_handlers=[sendPushBulletOnFail])
def gsheetsAuth():
    kLocalAuthFile = os.path.join('/','Users','danielegan','src','pifect','src', 'tweetbot', 'client_secrets.json')
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(kLocalAuthFile, scope)
    client = gspread.authorize(creds)
    return client


@task(name="getsheet", slug="getsheet", state_handlers=[sendPushBulletOnFail])
def getSheet(thisclient, spreadSheet, workSheet):
    sheet = thisclient.open(spreadSheet).worksheet(workSheet)
    return sheet

@task(name="convertSheetToPD", slug="convertSheetToPD", state_handlers=[sendPushBulletOnFail])
def convertSheetToPD(workSheet):
    posts = pd.DataFrame(workSheet.get_all_values())
    new_header = posts.iloc[0] #grab the first row for the header
    posts = posts[1:] #take the data less the header row
    posts.columns = new_header #set the header row as the df header
    return posts

@task(name="getNewPostIndex", slug="getNewPostIndex", state_handlers=[sendPushBulletOnFail])
def getNewPostIndex(posts):
    posts['LastPostedDT'] = pd.to_datetime(posts['LastPosted'])
    post_index = posts['LastPostedDT'].idxmin() # Get the index of the oldest row
    return post_index

@task(name="getNewPost", slug="getNewPost", state_handlers=[sendPushBulletOnFail])
def getNewPost(posts, post_index):
    new_post = posts.loc[post_index].Post # Get the post
    return new_post

@task(name="modifyTweet", slug="modifyTweet", state_handlers=[sendPushBulletOnFail])
def modifyTweet(tweet, hashtag):
    new_post = tweet + "\n\n#" + hashtag + "\n\n----\n#apbb"
    return new_post

@task(name="sendTweet", slug="sendTweet", state_handlers=[sendPushBulletOnFail])
def sendTweet(new_post, api):
    if (len(new_post) < 40):
        raise Exception("post is " + str(len(new_post)) + "chars: too short. Error?")
    else:
        status = api.PostUpdate(new_post)
    return status.text


@task(name="updatePostQueue", slug="updatePostQueue", state_handlers=[sendPushBulletOnFail])
def updatePostQueue(workSheet, post_index):
    today = date.today()
    workSheet.update_cell(post_index+1, 3, today.strftime("%Y/%m/%d"))

@task(name="sendPushBulletUpdate", slug="sendPushBulletUpdate")
def sendPushBulletUpdate(title, message):
    status = pb.push_note(title, message)
    return status


if __name__ == '__main__':
    load_creds()
    sendPushBulletOnFail()
    twitterAuth()
    gsheetsAuth()
    getSheet()
    convertSheetToPD()
    getNewPostIndex()
    getNewPost()
    modifyTweet()
    sendTweet()
    updatePostQueue()
    sendPushBulletUpdate()