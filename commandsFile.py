from app_config import officialURL, unofficialURL, VINofficial, VINunofficial
import requests

def sendOfficialRequest(url: str, headers: dict):
    try:
        response = requests.get(f"{officialURL}{url}", headers=headers)
        if response.status_code != 200:
            if response.status_code == 401:
                return False, {"error": "Unauthorized access. Please check your API key and access token."}
            return False,{"error": "Failed to retrieve data from official API.", "detail": response.json()}
        return True, response.json()
    except Exception as e:
        return False, {"error": str(e)}

def sendUnofficialRequest(url: str, headers: dict):
    try:
        response = requests.get(f"{unofficialURL}{url}", headers=headers)
        if response.status_code != 200:
            return False,{"error": "Failed to retrieve data from unofficial API.", "detail": response.json()}
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
    return responseOfficial, responseUnofficial


    