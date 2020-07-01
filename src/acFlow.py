from prefect import task, Flow, Parameter
import requests
from prefect.engine import signals
from prefect.engine.state import Success, Failed, Skipped
import uuid
from datetime import timedelta
from prefect.schedules import IntervalSchedule
import yaml
# from prefect.utilities.notifications import jira_notifier
from prefect.utilities.notifications.notifications import gmail_notifier
from prefect.tasks.secrets import PrefectSecret

DarkSkiesKey = PrefectSecret("DARK"),
kUser = PrefectSecret("KASAUSER"),
kSecret = PrefectSecret("KASASECRET")

# handler=jira_notifier(only_states=[Failed], options={'project': 'TEST', 'issuetype': {'name': 'Task'}, 'description': "Is it still working?"}, assignee='jhg.burner')

handler = gmail_notifier(only_states=[Failed])

@task(name="token", slug="token")
def getKasaToken(kUser, kSecret):
    kUser2 = ''.join(kUser)
    kSecret2 = ''.join(kSecret)
    payload = {
        "method": "login",
        "params": {
            "appType": "Kasa_Android",
            "cloudUserName": kUser2,
            "cloudPassword": kSecret2,
            "terminalUUID": str(uuid.uuid4()),
        },
    }
    response = requests.post(url="https://wap.tplinkcloud.com/", json=payload)

    obj = response.json()
    token = obj["result"]["token"]
    return token


@task(name="device", slug="device")
def getKasaDeviceList(token):
    payload = {"method": "getDeviceList"}
    device_list = requests.post(
        "https://wap.tplinkcloud.com?token={}".format(token), json=payload
    )

    deviceID = device_list.json()["result"]["deviceList"]  # [0]['deviceId']
    return deviceID


@task(name="modify", slug="modify")
def modifyKasaDeviceState(token, deviceID, deviceState):
    payload = {
        "method": "passthrough",
        "params": {
            "deviceId": deviceID,
            "requestData": '{"system":{"set_relay_state":{"state":'
            + str(deviceState)
            + "}}}",
        },
    }
    response = requests.post(
        url="https://use1-wap.tplinkcloud.com/?token={}".format(token), json=payload
    )


@task(name="target", slug="target")
def targetACState(local_temp, maxTemp):
    if local_temp <= maxTemp:
        return 0
    elif local_temp > maxTemp:
        return 1


@task(name="getTemp", slug="getTemp")
def getTemp(lat, long, apiK):
    apiK2 = ''.join(apiK)
    forecast = "https://api.darksky.net/forecast/{}/{},{}".format(apiK2, lat, long)
    data = requests.get(url=forecast)
    json_response = data.json()  
    u = json_response["hourly"]["data"]
    temp = u[0]["temperature"]
    return temp


simpleSchedule = IntervalSchedule(interval=timedelta(minutes=120))

with Flow("TempAC", schedule=simpleSchedule) as flow:
    maxtemp = Parameter("maxtemp", default=90)
    local_temp = getTemp(40.7135, -73.9859, DarkSkiesKey)
    target_state = targetACState(local_temp, maxtemp)
    local_token = getKasaToken(kUser, kSecret)
    local_device_list = getKasaDeviceList(local_token)
    # Basically, we only have one device..
    this_device_id = local_device_list[0]["deviceId"]
    # Finally, modify target state.
    # Perhaps should check if  different first.
    modifyKasaDeviceState(local_token, this_device_id, target_state)


# flow.run()
flow.register(project_name="Jenny")

# flow.deploy(project_name="Jenny")
# flow.visualize()

# flow.deploy(project_name="Temp")


# @task(name="try1", slug="try1")
# def trial():
#     if 1 > 2:
#         #raise signals.SUCCESS(message='turning off!')
#         return 0
#     elif 1 < 1:
#         #raise signals.SKIP(message='skipping!')
#         return 1


# f = Flow("UDTry", tasks=[trial])
# f.deploy("Temp")
