#!/usr/bin/python
# -*- coding: utf-8 -*-

from pydantic import BaseModel

class Message(BaseModel):
    sender: str
    targets: list # Id of receiver (in case of aws, classic)
    message: str
    protocol: str # Protocol dependent on provider
    topics: list 
    provider: str # Supported providers: aws, classic, firebase
