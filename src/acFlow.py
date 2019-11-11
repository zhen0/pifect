from prefect import task, Flow
from prefect.engine import signals
import requests
import uuid
from datetime import timedelta
import pendulum
from prefect import Flow
from prefect.schedules import IntervalSchedule
from prefect.schedules import CronSchedule
from prefect.schedules import Schedule
from prefect.schedules.clocks import IntervalClock
from prefect.environments.storage import Docker
import yaml

with open('credentials.yaml') as f:
    credentials = yaml.safe_load(f)

kUser = credentials["Jenny"]["kasa"]["userid"]
kSecret = credentials["Jenny"]["kasa"]["password"]
kDarkSkiesKey = credentials["Jenny"]["dark_skies"]["key"]
this_device_id = credentials["Jenny"]["kasa"]["device_id"]
#storage = Docker(
#    base_image="python:3.7",
#    python_dependencies=["requests", "uuid", "pendulum", "timedelta"],
#    registry_url="jenniferheleng",
#    image_name="temp",
#    image_tag="latest",
#)

@task
def getKasaToken(kUser, kSecret):
    payload = {
            "method": "login",
            "params": {
                "appType": "Kasa_Android",
                "cloudUserName": kUser,
                "cloudPassword": kSecret,
                "terminalUUID": str(uuid.uuid4())
            }
    }
    response = requests.post(url="https://wap.tplinkcloud.com/", json=payload)

    obj = response.json()
    token = obj["result"]["token"]
    return token

@task
def getKasaDeviceList(token):
    payload = {"method": "getDeviceList"}
    device_list = requests.post("https://wap.tplinkcloud.com?token={}".format(token), json=payload)
        # print("id", response2.json()['result']['deviceList'][0])
    deviceID = device_list.json()['result']['deviceList'] # [0]['deviceId']
    #print(deviceID[0]['deviceId'])
    return(deviceID)

@task
def modifyKasaDeviceState(token, deviceID, deviceState):
    payload = {
            "method": "passthrough",
            "params": {
                "deviceId": deviceID,
                "requestData":
                    '{\"system\":{\"set_relay_state\":{\"state\":' + str(deviceState) + '}}}'
            }
        }
    response = requests.post(url="https://use1-wap.tplinkcloud.com/?token={}".format(token), json=payload)
    #print(response.json())

@task
def targetACState(temp, minTemp, maxTemp):
    if temp <= maxTemp:
        #raise signals.SUCCESS(message='turning off!')
        return 0
    elif temp > maxTemp:
        #raise signals.SKIP(message='skipping!')
        return 1


@task
def getTemp(lat, long, apiK):
    forecast = 'https://api.darksky.net/forecast/{}/{},{}'.format(apiK, lat, long)
    data = requests.get(url=forecast)
    json_response = data.json()
    u = json_response[u'hourly'][u'data']
    temp = u[0][u'temperature']
    #print("temp", temp)
    return temp

#schedule = Schedule(clocks=[IntervalClock(timedelta(minutes=2))])
#chedule.next(1)
#simpleSchedule = IntervalSchedule(interval=timedelta(minutes=30))
daily_schedule = CronSchedule("* * * * *")

with Flow(daily_schedule) as flow:
    local_temp        = getTemp(40.7135, -73.9859, kDarkSkiesKey)
    target_state      = targetACState(local_temp, 80, 90)
    local_token       = getKasaToken(kUser, kSecret)
    local_device_list = getKasaDeviceList(local_token)
    this_device_id    = local_device_list[0]['deviceId'] # Basically, we only have one device..
    # Finally, modify target state.
    # Perhaps should check if  different first.
    modifyKasaDeviceState(local_token, this_device_id, target_state)


flow.run()
#flow.storage = storage
#flow.deploy(project_name="Temp")
