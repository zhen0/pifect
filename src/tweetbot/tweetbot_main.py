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
stream = open(os.path.join('/', 'Users', 'danielegan', 'src', 'degan_creds.yaml'), 'r')
creds = yaml.safe_load(stream)
twitter_creds = creds['twitter']
api = twitter.Api(consumer_key        = twitter_creds['consumer_key'],
                  consumer_secret     = twitter_creds['consumer_secret'],
                  access_token_key    = twitter_creds['access_token'],
                  access_token_secret = twitter_creds['access_token_secret'])
# Pushbullet
from pushbullet import Pushbullet
pb = Pushbullet(creds['pushbullet']['token'])

# Prefect
from prefect import task, Flow
from prefect.schedules import IntervalSchedule



# Autheticate
kLocalPath = os.path.join('/','Users','danielegan','src','pifect','src', 'tweetbot')
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(kLocalPath, 'client_secrets.json'), scope)
client = gspread.authorize(creds)


@task(name="getsheet", slug="getsheet")
def getSheet(spreadSheet, workSheet):
    sheet = client.open(spreadSheet).worksheet(workSheet)
    return sheet

@task(name="convertSheetToPD", slug="convertSheetToPD")
def convertSheetToPD(workSheet):
    posts = pd.DataFrame(workSheet.get_all_values())
    new_header = posts.iloc[0] #grab the first row for the header
    posts = posts[1:] #take the data less the header row
    posts.columns = new_header #set the header row as the df header
    return posts

@task(name="getNewPostIndex", slug="getNewPostIndex")
def getNewPostIndex(posts):
    posts['LastPostedDT'] = pd.to_datetime(posts['LastPosted'])
    post_index = posts['LastPostedDT'].idxmin() # Get the index of the oldest row
    return post_index

@task(name="getNewPost", slug="getNewPost")
def getNewPost(posts, post_index):
    new_post = posts.loc[post_index].Post # Get the post
    return new_post

@task(name="sendTweet", slug="sendTweet")
def sendTweet(new_post):
    if (len(new_post) < 20):
        status = "post too short. must be error"
        return status
    else:
        status = api.PostUpdate(new_post)
    return status.text

@task(name="updatePostQueue", slug="updatePostQueue")
def updatePostQueue(workSheet, post_index):
    today = date.today()
    workSheet.update_cell(post_index, 3, today.strftime("%Y/%m/%d"))


@task(name="sendPushBulletUpdate", slug="sendPushBulletUpdate")
def sendPushBulletUpdate(title, message):
    status = pb.push_note(title, message)
    return status


with Flow("Run BeFiWins") as flow:
    sheet               = getSheet("Twitter Posts", "BeFiWins")
    posts               = convertSheetToPD(sheet)
    post_index          = getNewPostIndex(posts)
    new_post            = getNewPost(posts, post_index)
    send_result         = sendTweet(new_post)
    update_sheet_result = updatePostQueue(sheet, post_index)
    update_message = flow.name + " ran: "
    send_PB_update      = sendPushBulletUpdate(update_message, send_result)

flow.run()