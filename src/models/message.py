from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    sender: str
    targets: list # Number of receiver
    message: str
    protocol: str # Usually: sms
    topic: str # (could be used for groupping notifications)
    provider: str # Supported providers: aws, classic
