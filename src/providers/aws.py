import boto3
import os

class AWS:

    client = boto3.client(
        "sns",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ['AWS_REGION']
    )

 
    def push(self, message):
        # Topic if it doesn't exist yet
        topic = self.client.create_topic(Name=message.topic)
        topic_arn = topic['TopicArn']

        # Subscribers
        for number in message.targets:
            self.client.subscribe(
                TopicArn=topic_arn,
                Protocol=message.protocol,
                Endpoint=number
            )

        # Publishing
        try:
            self.client.publish(
                Message=message.message,
                TopicArn=topic_arn
            )
        except Exception as e:
            print("Failed to publish message: ", e)
            return 1

        return 0
