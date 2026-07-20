import json

from app_config import officialURL, unofficialURL, VINofficial, VINunofficial
import requests

#post version needed
def sendOfficialRequest(url: str, headers: dict,method: str = "GET",body: dict = None):
    try:
        if method == "POST":
            if body is None:
                headers["Content-Type"] = "application/json"
                response = requests.post(f"{officialURL}{url}", headers=headers)
            else:
                response = requests.post(f"{officialURL}{url}", headers=headers, json=body)
                
        else:
            response = requests.get(f"{officialURL}{url}", headers=headers)
            
        return True, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def sendUnofficialRequest(url: str, headers: dict,method: str = "GET",body: dict = None):
    try:
        if method == "POST":
            if body is None:
                response = requests.post(f"{unofficialURL}{url}", headers=headers)
            else:
                response = requests.post(f"{unofficialURL}{url}", headers=headers, json=body)
        else:
            response = requests.get(f"{unofficialURL}{url}", headers=headers)

        return True, response.json()
    except Exception as e:
        return False, {"error": str(e)}


def headersGen(api_key: str, access_token: str):
    headers = {
        "vcc-api-key": api_key,
        "Authorization": f"Bearer {access_token}"
    }
    return headers

def get_locks(api_key_v: str, access_token: str,api_key_p: str):
    url = f"/vehicles/{VINofficial}/doors"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers)
    url= f"/vehicles/{VINunofficial}/doors"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers)
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)

def lock(api_key_v: str, access_token: str, api_key_p: str):
    url = f"/vehicles/{VINofficial}/commands/lock"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers, method="POST")
    url= f"/vehicles/{VINunofficial}/commands/lock"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers, method="POST")
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)

def unlock(api_key_v: str, access_token: str, api_key_p: str):
    url = f"/vehicles/{VINofficial}/commands/unlock"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers, method="POST")
    url= f"/vehicles/{VINunofficial}/commands/unlock"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers, method="POST")
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)

def get_engine_status(api_key_v: str, access_token: str, api_key_p: str):
    url = f"/vehicles/{VINofficial}/engine-status"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers)
    url= f"/vehicles/{VINunofficial}/engine-status"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers)
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)

def engine_start(api_key_v: str, access_token: str, api_key_p: str):
    body = {"runtimeMinutes": 10} 
    url = f"/vehicles/{VINofficial}/commands/engine-start"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers, method="POST", body=body)
    url= f"/vehicles/{VINunofficial}/commands/engine-start"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers, method="POST", body=body)
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)

def engine_stop(api_key_v: str, access_token: str, api_key_p: str):
    url = f"/vehicles/{VINofficial}/commands/engine-stop"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers, method="POST")
    url= f"/vehicles/{VINunofficial}/commands/engine-stop"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers, method="POST")
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)

def get_windows(api_key_v: str, access_token: str, api_key_p: str):
    url = f"/vehicles/{VINofficial}/windows"
    headers = headersGen(api_key_v, access_token)
    successOfficial, responseOfficial = sendOfficialRequest(url, headers)
    url= f"/vehicles/{VINunofficial}/windows"
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url, headers)
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)







def manual_command( api_key_v: str, access_token: str , api_key_p: str, url: str, method: str = "GET", body: str = None):
    headers = headersGen(api_key_v, access_token)
    url_official = url.replace("{VIN}", VINofficial)
    url_unofficial = url.replace("{VIN}", VINunofficial)
    successOfficial, responseOfficial = sendOfficialRequest(url_official, headers, method=method, body=body)
    headers=headersGen(api_key_p, "NOT NEEDED")
    successUnofficial, responseUnofficial = sendUnofficialRequest(url_unofficial, headers, method=method, body=body)
    return json.dumps(responseOfficial, indent=4), json.dumps(responseUnofficial, indent=4)