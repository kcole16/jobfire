import os
import time
import logging

import requests
from algoliasearch import algoliasearch

logger = logging.getLogger("error.logger")

def send_mail(subject, recipient, html, sender):
    r = requests.post(
        "https://api.mailgun.net/v2/%s/messages" % os.environ['MAILGUN_NAME'],
        auth=("api", os.environ['MAILGUN_API_KEY']),
        data={"from": "%s" % sender,
              "to": recipient,
              "subject": subject,
              "html": html})
    if not r.ok:
        logger.error(r.text)

def send_conf_email(student, email_token):
    subject = "Welcome to JobFire"
    sender = "kendall@jobfire.co"
    html = """<p>Hey %s,</p>
    <p>Welcome to JobFire! We are excited to help you find a great job or internship at one of our partner companies.
    <br>If you have any questions, feel free to contact me at kendall@jobfire.co.</p>
    <p>Before getting started, please click the below link to confirm your email:<br>
    <a href="https://www.jobfire.co/confirm_email/%s/">https://www.jobfire.com/confirm_email/%s/</a></p>
    <p>Best of luck</p>
    <p>Kendall<br>Co-Founder<br>JobFire, Inc.</p>""" % (student.first_name, email_token, email_token)
    send_mail(subject, student.email, html, sender)

def format_city(city):
    splits = city.split(',')
    formatted = "%s, %s" % (splits[0], splits[1])
    return formatted

