import tweet_flow_components as tfc
import os
from pushbullet import Pushbullet
from prefect import task, Flow, Task, Parameter
from prefect.schedules import IntervalSchedule

credentials_file = os.path.join('/', 'Users', 'danielegan', 'src','degan_creds.yaml')
creds = tfc.load_creds(credentials_file)
pb = Pushbullet(creds['pushbullet']['token'])

#BeFiWins
t = Task(state_handlers=[tfc.sendPushBulletOnFail])
with Flow(name="BeFiWins", tasks=[t]) as flow:
    spreadSheet = "Twitter Posts"
    workSheet = "BeFiWins"
    send_PB_update      = tfc.sendPushBulletUpdate(flow.name + " is running ", 'hi')
    twitter_api         = tfc.twitterAuth(creds)
    gs_client           = tfc.gsheetsAuth()
    sheet               = tfc.getSheet(gs_client, spreadSheet, workSheet)
    posts               = tfc.convertSheetToPD(sheet)
    post_index          = tfc.getNewPostIndex(posts)
    new_post            = tfc.getNewPost(posts, post_index)
    final_post          = tfc.modifyTweet(new_post, workSheet)
    send_result         = tfc.sendTweet(final_post, twitter_api)
    update_sheet_result = tfc.updatePostQueue(sheet, post_index)
    send_PB_update      = tfc.sendPushBulletUpdate(flow.name + " ran: ", send_result)

flow.run()