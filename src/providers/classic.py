#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
import os


class SMTPMail:

    try:
        SMTP_USER = os.environ['SMTP_USER']
        SMTP_HOST = os.environ['SMTP_HOST']
        SMTP_PORT = os.environ['SMTP_PORT']
        SMTP_PWD = os.environ['SMTP_PASSWORD']
    except Exception as e:
        print ('Classic credentials are not set as environment variables.', e)

    def send(self, message):
        sent_from = self.SMTP_USER
        to = message.targets
        subject = message.topic
        body = message.message

        email_text="""\
            From: %s
            To: %s
            Subject: %s


            %s
        """%(sent_from,",".join(to),subject, body)

        try:
            smtp_server = smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT)
            smtp_server.ehlo()
            smtp_server.login(self.SMTP_USER, self.SMTP_PWD)
            smtp_server.sendmail(sent_from, to[0], email_text)
            smtp_server.close()
            print("Mail was sent successfully.")
            return 0
        except Exception as e:
            print("Something went wrong when sending mail: ", e)
            return 1


def push(message):

    # Extend when add more message types for the "classic" provider

    switcher = {'email': SMTPMail()}

    sender = switcher.get(message.protocol, lambda : \
                          'This message protocol is not yet supported for this provider')
    result = sender.send(message)
    return result
