import tweet_flow_components as tfc
import os
from pushbullet import Pushbullet
from prefect import task, Flow, Task, Parameter
from prefect.schedules import IntervalSchedule, CronSchedule

credentials_file = os.path.join('/', 'Users', 'danielegan', 'src','degan_creds.yaml')
creds = tfc.load_creds(credentials_file)
pb = Pushbullet(creds['pushbullet']['token'])
t = Task(state_handlers=[tfc.sendPushBulletOnFail])

# Schedules
befiwins_schedule = CronSchedule("50 7 * * mon,wed")
befifails_schedule = CronSchedule("15 12 * * tue,thu")
dpegan_schedule = CronSchedule("15 8 * * wed,sat")

#BeFiWins
with Flow(name="twitterbot", tasks=[t]) as this_flow:
    spreadSheet         = Parameter("spreadsheet")
    workSheet           = Parameter('workSheet')
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
    send_PB_update      = tfc.sendPushBulletUpdate(workSheet + " ran: ", send_result)


this_flow.run(parameters = dict(spreadSheet = "Twitter Posts", workSheet = "BeFiFails"))

this_flow.run(parameters = dict(spreadSheet = "Twitter Posts", workSheet = "BeFiFails"))