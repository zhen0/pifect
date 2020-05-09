from jira import JIRA
from prefect import task, Flow, Parameter
from prefect.tasks.secrets import PrefectSecret


# jiraToken = PrefectSecret('JIRATOKEN')
jiraToken = "1Qd4yIwxdW3MMBMh9vTh3DAF"


@task
def addJiraticket(token, project_name, serverURL):
    
    jira = JIRA(basic_auth=('jjeennyygg@gmail.com',
                            token), options={'server': serverURL})
    
    # sdi = {"id": "3"},
    # rti = {'name': 10010},
    summary = "working",
    description= "kdjsfg"


    options = {    
    "serviceDeskId": "4",
    "requestTypeId": 10020,
    "requestFieldValues": {
        "summary": "Request JSD help via jsd task",
        "description": "I need a ne mouse for my Mac"
    },
    "assignee": "Jenny G"
}
        

    issue = jira.create_customer_request(
        options)

    
    


with Flow('jiraTicket') as fl:
    addJiraticket(jiraToken, "JSD", 
    'https://testjg22.atlassian.net')

fl.run()
