from prefect import task, Flow, Parameter
import time

@task
def sleep(x):
    time.sleep(x)
@task
def plus1(x):
    print(x+1)
    return x+1


with Flow(name='I sleep for param') as flow:
    x = Parameter('x', default = 5)
    sleep(x=x)
    plus1(2)

assert plus1.value == 3
flow.run()
# flow.register('Jenny')


# from prefect import task, Flow, Parameter
# from prefect.environments.storage import Docker
# from prefect.schedules import Schedule
# from datetime import timedelta
# from prefect.schedules.clocks import IntervalClock
# import pendulum
# import time
# from prefect.tasks.notifications import PushbulletTask
# from pushbullet import Pushbullet
# from prefect.tasks.secrets import PrefectSecret
# from prefect.tasks.notifications import EmailTask

# pbtoken = PrefectSecret("PUSHBULLET_TOKEN")

# PushbulletTask('wr')
# EmailTask('test1')

# @task
# def print_plus_one(x, pbtoken):
#     # EmailTask('test2')
#     # pb = Pushbullet(pbtoken)


#     #     # send the request
#     # resp = pb.push_note('Flow Notification', 'working22')
#     # print('resp', resp)
#     time.sleep(x)
#     print(x)
    
# sendPB = PushbulletTask('working')
    
# # schedule = Schedule(clocks=[IntervalClock(start_date=pendulum.now(),
# #     interval=timedelta(days=1))])


# with Flow(name='I sleep for param') as flow:
#     sendPB('working 234')
#     # PushBulletTask.run()
#     # EmailTask(subject='t5')
#     x = Parameter('x', default = 8)
#     print_plus_one(x, pbtoken)
    
    
    

# # flow.run(parameters=dict(x=1)) # prints 2
# # flow.run(parameters=dict(x=100)) # prints 101
# # flow.run() #prints 3

# # flow.storage = Docker(
# #     base_image="python:3.7",
# #     registry_url="jenniferheleng",
# #     image_name="temp",
# #     image_tag="latest",
# #     python_dependencies=['jira']
# # )


# flow.register()


# from prefect import Flow, Parameter
# from prefect.tasks.jira.jira_task import JiraTask
# from prefect.tasks.notifications import PushbulletTask

# def test_meta_model_regression():
#     meta_model_run = meta_model_flow.run(
#         db = "test.db",
#     )
#     assert meta_model_run.message == "All reference tasks succeeded."
# models = JiraTask(server_url = 'https://testjg.atlassian.net',
#         project_name = 'TEST',
#         summary = "Test my jira task")

# models2 = PushbulletTask(msg = "hello")

# with Flow("meta_model_flow") as meta_model_flow:
#     db = Parameter('db', default='db')
#     models()