import os
import time
import logging
import json
import locale

from apps.profile.models import Company

import requests
from algoliasearch import algoliasearch
from bs4 import BeautifulSoup
import pymongo

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
    subject = "Welcome to EntryWire"
    sender = "Kendall Cole at EntryWire <kendall@entrywire.com>"
    html = """<p>Hello,</p>
    <p>Welcome to EntryWire! We are excited to help you find a great job or internship at one of our partner companies.
    <br>If you have any questions, feel free to contact me at kendall@entrywire.com.</p>
    <p>Before getting started, please click the below link to confirm your email:<br>
    <a href="https://www.entrywire.com/confirm_email/%s/">https://www.entrywire.com/confirm_email/%s/</a></p>
    <p>Best of luck,</p>
    <p>Kendall<br>Co-Founder<br>EntryWire, Inc.</p>""" % (email_token, email_token)
    send_mail(subject, student.email, html, sender)

def format_city(city):
    splits = city.split(',')
    formatted = "%s, %s" % (splits[0], splits[1])
    return formatted

def authenticate_linkedin(code):
    url = 'https://www.linkedin.com/uas/oauth2/accessToken'
    client_id = os.environ['LINKEDIN_CLIENT_ID']
    client_secret = os.environ['LINKEDIN_CLIENT_SECRET']
    data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': '%s/oauth/' % str(os.environ['PATH_URL']),
    'code': code,
    'grant_type': 'authorization_code'
    }
    r = requests.post(url, data=data)
    access_token = r.json()['access_token']
    return access_token

def try_attribute(xml, attribute):
    try:
        attribute = xml.find(attribute).string
    except AttributeError:
        attribute = None
    return attribute

def parse_profile(profile):
    xml = BeautifulSoup(profile)
    picture_url = try_attribute(xml, 'picture-url')
    profile = try_attribute(xml, 'public-profile-url')
    first_name = try_attribute(xml, 'first-name')
    last_name = try_attribute(xml, 'last-name')
    user_details = {
        'profile':profile, 
        'picture_url':picture_url,
        'first_name':first_name,
        'last_name':last_name
        }   
    return user_details

def save_linkedin_profile(student, access_token):
    url = 'https://api.linkedin.com/v1/people/~:(id,public-profile-url,first-name,last-name,picture-url)'
    headers = {
        'Host':'api.linkedin.com',
        'Connection':'Keep-Alive',
        'Authorization': 'Bearer %s' % access_token
    }
    r = requests.get(url, headers=headers)
    if r.ok:
        user_details = parse_profile(r.text)
        student.picture = user_details['picture_url']
        student.linkedin = user_details['profile']
        student.first_name = user_details['first_name']
        student.last_name = user_details['last_name']
        student.save()

def slack_notification(channel, text):
    payload = {"channel": "#%s" % channel, "username": "Marvin","text":text}
    url = "https://hooks.slack.com/services/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"
    r = requests.post(url, json=payload)

def connect_db():
    client = pymongo.MongoClient(os.environ['MONGO_URL'])
    if os.environ['PRODUCTION'] == 'False':
        db = client['entrywire-data']
    else:
        db = client['entrywire-data']
    return db

def get_company_info(name):
    db = connect_db()
    locale.setlocale( locale.LC_ALL, 'en_US' )
    company_info = db.companies.find_one({'name':name})
    if company_info:
        try:
            company_info['total_funding'] = locale.currency(int(company_info['total_funding']), grouping=True)
        except (KeyError, TypeError):
            company_info['total_funding'] = 'N/A'
        try:
            stage = company_info['funding_stage']
        except (KeyError, TypeError):
            company_info['funding_stage'] = 'Seed'
        else:
            if stage == 'PreSeriesA' or stage == 'Pre Series A':
                company_info['funding_stage'] = 'Seed'
            elif stage == '':
                company_info['funding_stage'] = 'Seed'
            else:
                company_info['funding_stage'] = 'Series %s' % stage
    else:
        company = Company.objects.get(name=name)
        company_info = {}
        company_info['name'] = company.name
        company_info['logo_url'] = company.logo
        company_info['high_concept'] = ""
        company_info['product_desc'] = company.about
        company_info['total_funding'] = "Undisclosed"
        company_info['funding_stage'] = "N/A"
        company_info['employees'] = ""
    return company_info






