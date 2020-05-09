import requests
url = "https://zillowdimashirokovv1.p.rapidapi.com/GetSearchResults.htm"
payload = "chartDuration=1year&chartDuration=5years&chartDuration=10years&zpid=48327876&unit-type=dollar&zws-id=X1-ZWz178kx96hfyj_7oq0o&citystatezip=12472&address=298-Mountain-Rd-Rosendale-NY"
headers = {
    'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
    "x-rapidapi-key": "ee0bec7d04msh70b389348a1a0f9p192017jsn46eafeafec8f",
    'content-type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)

