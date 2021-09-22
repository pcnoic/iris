#!/usr/bin/python
# -*- coding: utf-8 -*-

from firebase_admin.credentials import Base
from pydantic import BaseModel

class Telephone(BaseModel):
    telephone_numbers: list
    topic: str
