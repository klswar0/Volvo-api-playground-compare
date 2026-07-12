from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel, Field 
from fastapi import FastAPI, Query, Response, Request, Header
from fastapi.responses import JSONResponse, FileResponse
import requests
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

page="http://localhost:8000"


class auth(BaseModel):
    api_key_play: str = Field(...) 

    api_key_sand:str = Field(...)
    access_token: str = Field(...)

database = {"test": {auth}}


@app.get("/")
def index():
    return FileResponse("templates/index.html")

@app.get("/login")
def login(request: Request, api_key: str = Query(default=None), playground_login: bool = Query(default=False)):
    return templates.TemplateResponse(
        name="login.html",
        context={"api_key": api_key, "playground_login": playground_login},
        request=request
    )


@app.get("/login/automatic")
def login_automatic():
    try:
        url=f"{page}/internal/APIKey"
        response = requests.get(url)
        api_key = response.json().get("message")
        print(f"Retrieved API key: {api_key}")
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to retrieve API key.","detail": response.json()}) #html
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    try:
        url=f"{page}/internal/addCar"
        header = {"vcc-api-key": api_key}
        body={"VIN": "YV1RZ4CL3M1000001DEMO",
            "attributes": {"fuelICE": 120, "fuelElectric": 80, "odometer": 10000, "oillevel": "TOO_LOW", "hazardLightsWarning": "FAILURE","frontLeft": "VERY_LOW_PRESSURE","frontRight": "LOW_PRESSURE","rearLeft": "UNSPECIFIED","rearRight": "NO_WARNING"}}
        response = requests.post(url, headers=header, json=body)
        if response.status_code != 200:
            return JSONResponse(content={"error": "Failed to add car.","detail": response.json()}) #html
        response=Response()
        response.headers["HX-Redirect"] = f"/login?api_key={api_key}&playground_login=True"
        return response
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    
    return JSONResponse(content={"message": "Automatic login successful. Car added."})

@app.get("/login/manual")
def login_manual(api_key: str, access_token: str):
    try:
        url=f"https://api.volvocars.com/connected-vehicle/v2/vehicles"
        headers = {"vcc_api_key": api_key, "Authorization": access_token}
        response = requests.get(url, headers=headers)
        vehicles = response.json()
        # Check if the response contains vehicles or an error message

        return JSONResponse(content={"Check": True})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
    
uvicorn.run(app,port=8001)