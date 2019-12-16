from jira import JIRA
from prefect import task, Flow, Parameter
from prefect.tasks.secrets import Secret

jiraToken = Secret('JIRATOKEN')


@task
def addJiraticket(token, projectName, summaryText, issueType, serverURL):
    jira = JIRA(basic_auth=('jjeennyygg@hotmail.com',
                            token), options={'server': serverURL})
    jira.create_issue(
        project=projectName, summary=summaryText, issuetype={'name': issueType})


with Flow('jiraTicket') as fl:
    addJiraticket(jiraToken, 'TEST', "Testing w secrets", 'Task',
    'https://testjg.atlassian.net')

fl.run()
# def sendPushBulletOnFail(task, old_state, new_state):
#     if new_state.is_failed():
#         msg = "{0} failed in state {1}".format(task, new_state)
#         pb.push_note('Flow Error', msg)
#     return new_state


# t = Task(state_handlers=[sendPushBulletOnFail])
