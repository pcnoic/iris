#!/usr/bin/python
# -*- coding: utf-8 -*-

from firebase_admin.credentials import Base
from pydantic import BaseModel

class Device(BaseModel):
    registration_tokens: list
    topic: str
