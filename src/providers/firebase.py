#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests



class FIREBASE_PUSH:
    try:
        notification_api = os.environ["FIREBASE_PUSH_API"]
        print(notification_api)
    except Exception as e:
        print("The Firebase API is not set as environment variable: ", e)

    try:
        firebase_server_key = os.environ["FIREBASE_SERVER_KEY"]
        print(firebase_server_key)
    except Exception as e:
        print("The Firebase Server Key is not set", e)


    try:
        application_url = os.environ["APPLICATION_URL"]
        print(application_url)
    except Exception as e:
        print("The application url is not set for Firebase notifications", e)


    def send(self, message):
        """
        Publishes a push notification payload to Firebase Cloud Messaging.

        :param message: The message object to use.
        :return The ID of the message.
        """

        headers = {
            "Authorization": "Bearer " + self.firebase_server_key,
            "Content-Type": "application/json"
        }

        notification = {
            "title": message.topic,
            "body": message.message,
            "click_action": self.application_url
        }




        for target in message.targets:

            payload = {}

            payload = {
                "notification": notification,
                "to": target,
            }

            try:
                print(payload)
                print(headers)
                req = requests.post(self.notification_api, json=payload, headers=headers)
                print(req.status_code, req.reason, req.json())
            except Exception as e:
                print("Something went wrong when sending a request to Firebase Push API")
                return 1
            else: 
                return 0

def push(message):
    # Extend when adding more message types for the "firebase" provider
    switcher = {
        'push': FIREBASE_PUSH()
    }

    sender = switcher.get(message.protocol, lambda : 'This message protocol is not yet supported for this provider.')
    result = sender.send(message)
    return result
