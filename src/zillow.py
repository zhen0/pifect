import requests
url = "https://zillowdimashirokovv1.p.rapidapi.com/GetSearchResults.htm"
payload = "
headers = {
    'x-rapidapi-host': "ZillowdimashirokovV1.p.rapidapi.com",
    "x-rapidapi-key": 
    'content-type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)

