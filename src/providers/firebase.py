#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import firebase_admin
from firebase_admin import credentials, messaging
from fastapi.logger import logger
import sys

cred = credentials.Certificate("firebase_private_key.json")
# local testing
#cred = credentials.Certificate("firebase.json")

firebase_admin.initialize_app(cred)


class FIREBASE_REGISTER:

    """
    Registers devices in a notification topic.

    @param registration_tokens array
    @param topic string
    """
    def register_device(self, registration_tokens, topics):
        # Subscribe the devices corresponding to the registration tokens to the
        # topic.
        
        for topic in topics:
            response = messaging.subscribe_to_topic(registration_tokens, topic)
            sys.stdout.flush()
            if response.success_count > 0:
                print(response.success_count, ' tokens were subscribed to ', topic)
                
            else:
                return 1
        return 0

    """
    Unregisters devices from a notification topic.

    @param registration_tokens array
    @param topic string
    """
    def unregister_device(self, registration_tokens, topics):
        # Unubscribe the devices corresponding to the registration tokens from the
        # topic.
        
        for topic in topics:    
            response = messaging.unsubscribe_from_topic(registration_tokens, topic)
            sys.stdout.flush()
            if response.success_count > 0: 
                print(response.success_count, ' tokens were unsubscribed from ', topic)
                
            else:    
                return 1
        return 0
       

class FIREBASE_PUSH:

    try:
        application_url = os.environ["APPLICATION_URL"]
    except Exception as e:
        logger.error("APPLICATION_URL was not set. Notifications may malfanction.")

    def send(self, message):
        """
        Publishes a push notification payload to Firebase Cloud Messaging.

        :param message: The message object to use.
        :return The ID of the message.
        """

        notification = {
            "title": message.sender,
            "body": message.message,
            "click_action": self.application_url
        }

        topic = ""
        # Creating a computable topic expression
  
        for t in message.topics:
            topic = "'" + t + "' in topics && " + topic
        topic = topic[:-3]
        

        # Define a message payload
        payload = messaging.Message(
            notification,
            condition=topic
        )

        # Send message to the devices subscribed to the provided topic.
        response = messaging.send(payload)
        # Response is a message ID string
        sys.stdout.flush()
        if response is not None:
            print('Successfully sent message: ', response)
            return 0
        else:
            return 1
        


def push(message):
    # Extend when adding more message types for the "firebase" provider
    switcher = {
        'push': FIREBASE_PUSH()
    }

    sender = switcher.get(message.protocol, lambda : 'This message protocol is not yet supported for this provider.')
    result = sender.send(message)
    sys.stdout.flush()
    return result
