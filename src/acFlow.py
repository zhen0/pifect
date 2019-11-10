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


storage = Docker(
    base_image="python:3.7",
    python_dependencies=["requests", "uuid", "pendulum", "timedelta"],
    registry_url="jenniferheleng",
    image_name="temp",
    image_tag="latest",
)

@task
def getTemp(lat, long):
forecast = 'https://api.darksky.net/forecast/{}/{},{}'.format(apiK, lat, long)
    data = requests.get(url=forecast)
    json_response = data.json()
    u = json_response[u'hourly'][u'data']
    temp = u[0][u'temperature']
    print("temp", temp)
    return temp


@task
def ACoff(temp, maxTemp):
    if temp <= maxTemp:
        raise signals.SUCCESS(message='turning off!')
        payload = {
            "method": "login",
            "params": {
                "appType": "Kasa_Android",
                "cloudUserName": kUser,
                "cloudPassword": kSecret,
                "terminalUUID": str(uuid.uuid4())
            }
        }

        response = requests.post(url="https://wap.tplinkcloud.com/",
                                 json=payload)

        obj = response.json()
        print('obj', obj)
        token = obj["result"]["token"]
        print(token)

        payload = {"method": "getDeviceList"}
        response2 = requests.post(
            "https://wap.tplinkcloud.com?token={}".format(token), json=payload)
        # print("id", response2.json()['result']['deviceList'][0])
        deviceID = response2.json()['result']['deviceList'][0]['deviceId']

        payload3 = {
            "method": "passthrough",
            "params": {
                "deviceId": deviceID,
                "requestData":
                "{\"system\":{\"set_relay_state\":{\"state\":0}}}"
            }
        }
        response3 = requests.post(
            url="https://use1-wap.tplinkcloud.com/?token={0}".format(token),
            json=payload3)

        print(response3.json())

    elif temp > maxTemp:
        raise signals.SKIP(message='skipping!')

@task
def ACon(temp, minTemp):
    if temp >= minTemp:
        raise signals.SUCCESS(message='turning on!')
        payload = {
            "method": "login",
            "params": {
                "appType": "Kasa_Android",
                "cloudUserName": kUser,
                "cloudPassword": kSecret,
                "terminalUUID": str(uuid.uuid4())
            }
        }

        response = requests.post(url="https://wap.tplinkcloud.com/",
                                 json=payload)

        obj = response.json()
        print('obj', obj)
        token = obj["result"]["token"]
        print(token)

        payload = {"method": "getDeviceList"}
        response2 = requests.post(
            "https://wap.tplinkcloud.com?token={}".format(token), json=payload)
        # print("id", response2.json()['result']['deviceList'][0])
        deviceID = response2.json()['result']['deviceList'][0]['deviceId']

        payload3 = {
            "method": "passthrough",
            "params": {
                "deviceId": deviceID,
                "requestData":
                "{\"system\":{\"set_relay_state\":{\"state\":0}}}"
            }
        }
        response3 = requests.post(
            url="https://use1-wap.tplinkcloud.com/?token={1}".format(token),
            json=payload3)

        print(response3.json())

    elif temp < minTemp:
        raise signals.SKIP(message='skipping!')


schedule = Schedule(clocks=[IntervalClock(timedelta(minutes=2))])
schedule.next(1)
simpleSchedule = IntervalSchedule(interval=timedelta(minutes=30))
daily_schedule = CronSchedule("38 1 * * *")

with Flow('Nov10', simpleSchedule) as flow:
    temp1 = getTemp(40.7135, -73.9859)
    # temp2 = getTemp(23.401711, -90.750069)
    ACoff(temp1, 80)
    ACon(temp1, 90)
# flow.run()
flow.storage = storage
flow.deploy(project_name="Temp")
