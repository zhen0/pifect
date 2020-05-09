from prefect import task, Flow, Parameter
from prefect.environments.storage import Docker

import os
import time

from jira import JIRA
from prefect.tasks.secrets import Secret

jiraToken = Secret('JIRATOKEN')

@task
def print_plus_one(x):
    time.sleep(x)
    bob = os.environ.get("DOCKER_HOST", "<unix://var/run/docker.sock>")
    print(bob)
    print(x + 1)
    return bob

@task
def addJiraticket(token, projectName, summaryText, des, issueType, serverURL):
    jira = JIRA(basic_auth=('jjeennyygg@hotmail.com',
                            token), options={'server': serverURL})
    jira.create_issue(
        project=projectName, summary=summaryText, description=des, issuetype={'name': issueType})




with Flow(name='I am new') as flow:
    x = Parameter('x', default = 5)
    bobb = print_plus_one(x=x)
    addJiraticket(jiraToken, 'TEST', 'Testing March 9pm', bobb, 'Task',
    'https://testjg.atlassian.net')
    

# flow.run(parameters=dict(x=1)) # prints 2
# flow.run(parameters=dict(x=100)) # prints 101
# flow.run() #prints 3

# flow.storage = Docker(
#     base_image="python:3.7",
#     registry_url="jenniferheleng",
#     image_name="temp",
#     image_tag="latest",
#     python_dependencies=['jira']
# )


flow.register('Jenny')
