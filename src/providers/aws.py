#!/usr/bin/python
# -*- coding: utf-8 -*-
import boto3
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class AWS_SMS:

    try:
        client = boto3.client('sns',
                              aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], 
                              region_name=os.environ['AWS_REGION'])
    except Exception as e:
        print ('AWS credentials are not set as environment variables: ', e)

    def send(self, message):
        """
        Publishes a text message directly to a phone number without need for a
        subscription.

        :param phone_number: The phone number that receives the message. This must be
                             in E.164 format. For example, a United States phone
                             number might be +12065550101.
        :param message: The message to send.
        :return: The ID of the message.
        """

        for target in message.targets:

            try:
                response = self.client.publish(PhoneNumber=target, Message=message.message)
                message_id = response['MessageId']
                logger.info("Published message to %s.", target)
                print(message_id)
            except ClientError:
                logger.exception("Couldn't publish message to %s.", target)
                return 1
            else:
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
