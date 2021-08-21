#!/usr/bin/python
# -*- coding: utf-8 -*-
import boto3
import os


class AWS_SMS:

    try:
        client = boto3.client('sns',
                              aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'
                              ],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'
                              ], region_name=os.environ['AWS_REGION'])
    except Exception, e:
        print ('AWS credentials are not set as environment variables: '
               , e)

    def send(self, message):
        print message

        # Topic if it doesn't exist yet

        topic = self.client.create_topic(Name=message.topic)
        topic_arn = topic['TopicArn']

        # Subscribers

        for number in message.targets:
            self.client.subscribe(TopicArn=topic_arn,
                                  Protocol=message.protocol,
                                  Endpoint=number)

        # Publishing

        try:
            self.client.publish(Message=message.message,
                                TopicArn=topic_arn)
        except Exception, e:
            print ('Failed to publish message as SMS: ', e)
            return 1

        return 0


class AWS_SES:

    # TODO: implement methods

    def hello():
        print 'hello'


def push(message):

    # Extend when adding more message types for the "aws" provider

    switcher = {'sms': AWS_SMS(), 'email': AWS_SES()}

    sender = switcher.get(message.protocol, lambda : \
                          'This message protocol is not yet supported for this provider.')
    sender.send(message)
