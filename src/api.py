"""
iris - mobile message publisher
MIT LICENSE
"""

from fastapi import FastAPI
import json

from models.message import Message
from models.device import Device
from providers import aws, classic, firebase

# Application controllers
app = FastAPI()

# Initiate Providers
def aws_provider():
    return aws

def classic_provider():
    return classic

def firebase_provider():
    return firebase

# Endpoints
@app.post("/api/v1/message/push")
def push_message(message: Message):
    provider = None
    # Extend the switcher when adding providers
    switcher = {
        "aws": aws_provider(),
        "classic": classic_provider(),
        "firebase": firebase_provider(),
    }

    provider = switcher.get(message.provider, lambda: "Not supported provider")
    
    
    result = provider.push(message)
    if result == 0:
        response = {"status":"success"}
    else:
        response = {"status":"fail"}

    return response

@app.post("/api/v1/push/device/register")
def device_register(device: Device):
    registrar = firebase.FIREBASE_REGISTER()
    result = registrar.register_device(device.registration_tokens, device.topic)
    if result != 0:
        response = {"status":"fail"}
    else:
        response = {"status":"success"}
    
    return response


@app.post("/api/v1/push/device/unregister")
def device_unregister(device: Device):
    registrar = firebase.FIREBASE_REGISTER()
    result = registrar.unregister_device(device.registration_tokens, device.topic)
    if result != 0:
        response = {"status":"fail"}
    else: 
        response = {"status":"success"}
    
    return response
