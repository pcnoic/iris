#!/usr/bin/python
# -*- coding: utf-8 -*-
import boto3
import os
import logging
from botocore.endpoint import Endpoint
from botocore.exceptions import ClientError
from starlette.responses import Response

logger = logging.getLogger(__name__)

try:
    client = boto3.client('sns',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], 
        region_name=os.environ['AWS_REGION'])
except Exception as e:
    print ('AWS credentials are not set as environment variables: ', e)

class AWS_REGISTER:
    
    """
    Registers telephone numbers in a sms topic.

    @param telephone_numbers array
    @param topic string
    """
    def register_telephone(self, telephone_numbers, topics):
        for topic in topics:
            # Create the topic if it doesn't exist (this is idempotent)
            sms_topic = client.create_topic(Name=topic)
            sms_topic_arn = sms_topic['TopicArn'] # gets its ARN

            # Add SMS Subscribers
            for number in telephone_numbers:

                try:
                    client.subscribe(
                        TopicArn=sms_topic_arn,
                        Protocol='sms',
                        Endpoint=number
                    )
                except Exception as e:
                    print("Something went wrong when subscribing: ",e)
                    return 1
        return 0

class AWS_SMS:

    def send(self, message):
        """
        Publishes a text message to a topic.
        """
        # Get topic ARN
        for topic in message.topics:

            try:
                sms_topic = client.create_topic(Name=topic)
                sms_topic_arn = sms_topic['TopicArn']  # get its Amazon Resource Name

                # Publish a message.
                response = client.publish(Message=message.message, TopicArn=sms_topic_arn)
                message_id = response['MessageId']
                print("Sent message with message_id:", message_id)
            except Exception as e:
                print("Something went wrong when sending to topic: ", e)
                return 1

        return 0
    

class AWS_SES:

    # TODO: implement methods

    def hello():
        print ("hello")


def push(message):

    # Extend when adding more message types for the "aws" provider

    switcher = {
        'sms': AWS_SMS(), 
        'email': AWS_SES()
    }

    sender = switcher.get(message.protocol, lambda : \
                          'This message protocol is not yet supported for this provider.')
    result = sender.send(message)
    
    return result
