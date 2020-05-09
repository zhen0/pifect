from jira import JIRA
from prefect import task, Flow, Parameter
from prefect.tasks.secrets import PrefectSecret
from prefect.tasks.jira.jira_service_desk import JiraServiceDeskTask


# jiraToken = PrefectSecret('JIRATOKEN')
jiraToken = "1Qd4yIwxdW3MMBMh9vTh3DAF"

# @task
# def addJiraticket(token, projectName, summaryText, issueType, serverURL):
    
#     jira = JIRA(basic_auth=('jjeennyygg@hotmail.com',
#                             token), options={'server': serverURL})


#     issue = jira.create_issue(
#         project=projectName, summary=summaryText, issuetype={'name': issueType}, assignee={'accountId':'5df7f5e4d501d70cb600cbb0'})

    
addJiraticket = JiraServiceDeskTask()


with Flow('jiraTicket') as fl:
    addJiraticket(access_token=jiraToken, username="jjeennyygg@gmail.com", service_desk_id="3", issue_type=10010, summary="Testing flow count May", description = "blah blah blah",
    server_url = 'https://testjg22.atlassian.net')

fl.run()

# fl.register("Jenny")
# def sendPushBulletOnFail(task, old_state, new_state):
#     if new_state.is_failed():
#         msg = "{0} failed in state {1}".format(task, new_state)
#         pb.push_note('Flow Error', msg)
#     return new_state


# t = Task(state_handlers=[sendPushBulletOnFail])
