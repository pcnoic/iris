#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os


class SMTPMail:

    try:
        SMTP_HOST = os.environ['SMTP_HOST']
        SMTP_PORT = os.environ['SMTP_PORT']
        SMTP_PWD = os.environ['SMTP_PASSWORD']
    except Exception, e:
        print ('Classic credentials are not set as environment variables.'
               , e)

    def send(self, message):

        # Create message object

        msg = MIMEMultipart()

        # Message parameters

        msg['From'] = message.sender
        msg['To'] = message.targets
        msg['Subject'] = message.topic

        msg.attach(MIMEText(message.message, 'plain'))

        srv = smtplib.SMTP(self.SMTP_HOST + ': ' + self.SMTP_PORT)
        srv.starttls()
        srv.login(msg['From'], self.SMTP_PWD)
        srv.sendmail(msg['From'], msg['To'], msg.as_string())
        srv.quit()


def push(message):

    # Extend when add more message types for the "classic" provider

    switcher = {'email': SMTPMail}

    sender = switcher.get(message.protocol, lambda : \
                          'This message protocol is not yet supported for this provider')
    sender.send(message)
