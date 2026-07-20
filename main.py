from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel, Field 
from fastapi import FastAPI, Query, Response, Request, Header
from fastapi.responses import JSONResponse, FileResponse
import requests
import json
import commandsFile
from app_config import officialURL, unofficialURL, VINofficial, VINunofficial

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class auth(BaseModel):
    api_key_play: str = Field(...) 

    api_key_sand:str = Field(...)
    access_token: str = Field(...)

database = {"test": {auth}}


@app.get("/")
def index():
    return FileResponse("templates/index.html")

@app.get("/login")
def login(request: Request, api_key_p: str = Query(default=None),api_key_v: str = Query(default=None), access_token: str = Query(default=None), state: int = Query(default=0)):
    if state == 0:
        data={"api_key_p": None, "api_key_v": None, "access_token": None, "state": state}
    elif state == 1:
        data={"api_key_p": api_key_p, "api_key_v": None, "access_token": None, "state": state}
    elif state == 2:
        data={"api_key_p": api_key_p, "api_key_v": api_key_v, "access_token": access_token, "state": state}
    return templates.TemplateResponse(
        name="login.html",
        context=data,
        request=request
    )


@app.get("/login/automatic")
def login_automatic():
    try:
        url=f"{unofficialURL}/internal/APIKey"
        response = requests.get(url)
        api_key = response.json().get("message")
        print(f"Retrieved API key: {api_key}")
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to retrieve API key.","detail": response.json()}) #html
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    try:
        url=f"{unofficialURL}/internal/addCar"
        header = {"vcc-api-key": api_key}
        body={"VIN": VINunofficial,
            "attributes": {"fuelICE": 120, "fuelElectric": 80, "odometer": 10000, "oillevel": "TOO_LOW", "hazardLightsWarning": "FAILURE","frontLeft": "VERY_LOW_PRESSURE","frontRight": "LOW_PRESSURE","rearLeft": "UNSPECIFIED","rearRight": "NO_WARNING"}}
        response = requests.post(url, headers=header, json=body)
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to add car.","detail": response.json()}) #html
        response=Response()
        response.headers["HX-Redirect"] = f"/login?api_key_p={api_key}&state=1"
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    
    return JSONResponse(content={"message": "Automatic login successful. Car added."})

@app.get("/login/manual")
def login_manual(api_key_v: str, access_token: str, api_key_p: str):
    try:
        url=f"{officialURL}/vehicles"
        token = access_token.strip()
        if not token.startswith("Bearer "):
            token = f"Bearer {token}"
        headers = {"VCC-API-KEY": api_key_v, "Authorization": token}
        response = requests.get(url, headers=headers)
        vehicles = response.json()
        print(f"Retrieved vehicles: {vehicles}")
        # Check if the response contains vehicles or an error message
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to retrieve vehicles.","detail": vehicles}) #html

        response=Response()
        response.headers["HX-Redirect"] = f"/login?api_key_p={api_key_p}&api_key_v={api_key_v}&access_token={access_token}&state=2"
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    
#compare is not going thru and api_key_p is set to None api key is repaired check
@app.get("/compare")
def compare(request: Request, api_key_v: str, access_token: str , api_key_p: str):
    return templates.TemplateResponse(
        name="compare.html",
        context={"api_key_v": api_key_v, "access_token": access_token, "api_key_p": api_key_p},
        request=request
    )


@app.get("/commands")
def get_commands(request: Request,api_key_v: str, access_token: str , api_key_p: str , command: str):
    if command == "locks":
        responses = commandsFile.get_locks(api_key_v, access_token, api_key_p)
    elif command == "lock":
        responses = commandsFile.lock(api_key_v, access_token, api_key_p)
    elif command == "unlock":
        responses = commandsFile.unlock(api_key_v, access_token, api_key_p)
    elif command == "engine":
        responses = commandsFile.get_engine_status(api_key_v, access_token, api_key_p)
    elif command == "engineStart":
        responses = commandsFile.engine_start(api_key_v, access_token, api_key_p)
    elif command == "engineStop":
        responses = commandsFile.engine_stop(api_key_v, access_token, api_key_p)
    elif command == "windows":
        responses = commandsFile.get_windows(api_key_v, access_token, api_key_p)
    return templates.TemplateResponse(
            name="terminalOutput.html",
            context={"responses": responses, "official_response": responses[0], "unofficial_response": responses[1]},
            request=request
        )
    

@app.get("/manual")
def manual(request: Request, api_key_v: str, access_token: str , api_key_p: str):
    return templates.TemplateResponse(
        name="compareManual.html",
        context={"api_key_v": api_key_v, "access_token": access_token, "api_key_p": api_key_p, "VINofficial": VINofficial, "VINunofficial": VINunofficial},
        request=request
    )

@app.get("/manual/command")
def manual_command(request: Request, api_key_v: str, access_token: str , api_key_p: str, url: str, method: str = "GET", body: str = None):
    if body:
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return JSONResponse(content={"error": "Invalid JSON in request body."})
    data= commandsFile.manual_command(api_key_v, access_token, api_key_p, url, method, body)
    return templates.TemplateResponse(
        name="terminalOutput.html",
        context={"official_response": data[0],"unofficial_response": data[1]},
        request=request
    )


uvicorn.run(app,port=8001)