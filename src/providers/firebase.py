#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import requests

logger = logging.getLogger(__name__)

class FIREBASE_PUSH:
    try:
        notification_api = os.environ["FIREBASE_PUSH_API"]
    except Exception as e:
        print("The Firebase API is not set as environment variable: ", e)

    try:
        firebase_server_key = os.environ["FIREBASE_SERVER_KEY"]
    except Exception as e:
        print("The Firebase Server Key is not set")


    try:
        application_url = os.environ["APPLICATION_URL"]
    except Exception as e:
        print("The application url is not set for Firebase notifications")


    def send(self, message):
        """
        Publishes a push notification payload to Firebase Cloud Messaging.

        :param message: The message object to use.
        :return The ID of the message.
        """

        headers = {
            "Authorization": "Bearer: " + self.firebase_server_key,
            "Content-Type": "application/json"
        }

        notification = {
            "title": message.topic,
            "body": message.message,
            "click_action": self.application_url
        }



        for target in message.targets:

            payload = {
                "notification": notification,
                "to": target,
            }

            try:
                req = requests.post(self.notification_api, data=payload, headers=headers)
            except Exception as e:
                print("Something went wrong when sending a request to Firebase Push API")
