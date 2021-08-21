"""
iris - mobile message publisher
MIT LICENSE
"""

from fastapi import FastAPI
import json

from models.message import Message
from providers import aws, classic

# Application controllers
app = FastAPI()

# Initiate Providers
def aws_provider():
    return aws

def classic_provider():
    return classic

# Endpoints
@app.post("/api/v1/message/push")
def push_message(message: Message):
    provider = None
    # Extend the switcher when adding providers
    switcher = {
        "aws": aws_provider(),
        "classic": classic_provider()
    }

    provider = switcher.get(message.provider, lambda: "Not supported provider")
    
    
    result = provider.push(message)
    if result == 0:
        response = json.dumps({"status":"success"})
    else:
        response = json.dumps({"status":"failed"})

    return response

