from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.db import IntegrityError, connection, transaction
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from apps.profile.models import Student
from apps.profile.utils import send_mail
from apps.referrals.models import Referral

from datetime import datetime

import os
import uuid
import urllib
import requests
import json
from bs4 import BeautifulSoup


def authenticate_google(code):
    url = 'https://www.googleapis.com/oauth2/v3/token'
    client_id = os.environ['GOOGLE_CLIENT_ID']
    client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': '%s/oauth2callback/' % os.environ['PATH_URL'],
    'code': code,
    'grant_type': 'authorization_code'
    }
    r = requests.post(url, data=data)
    access_token = r.json()['access_token']
    return access_token

def get_contacts(student, access_token):
    headers = {'GData-Version': '3.0', 'Authorization': 'Bearer '+access_token}
    url = "https://www.google.com/m8/feeds/contacts/default/thin?max-results=100000"
    r = requests.get(url, headers=headers)
    xml = BeautifulSoup(r.text)
    entries = xml.find_all('entry')
    results = []
    previous_referrals = Referral.objects.all().values_list('email', flat=True).order_by('id')
    if previous_referrals.count() < 1:
        previous_referrals = []
    for entry in entries:
        name = entry.find('title').string
        email = entry.find('gd:email')['address']
        if email.split('@')[1] == student.university.email_ext and name != None and email not in previous_referrals:
            results.append({'name':name, 'email':email})
    return results

@csrf_exempt
def contact_referrals(request):
    student = Student.objects.get(user=request.user)
    referrals = json.loads(request.POST.dict()['data'])
    for referral in referrals:
        html = """<p>Hey %s,</p>
        <p>My name is Kendall, and I'm the founder of EntryWire. %s %s recently signed up with us, and thinks you'd be interested as well.</p>
        <p>We work with dozens of startups, many of which are actively recruiting %s students. If you'd like to see which ones, sign up <a href="https://www.entrywire.com/student_signup/">here</a>.<br>
        <p>Best of luck,</p>
        <p>Kendall<br>Co-Founder<br>EntryWire, Inc.</p>""" % (str(referral['name']).split(' ')[0], student.first_name, student.last_name,
            student.university.name)
        subject = "Startup Jobs for %s Students" % student.university.name
        sender = "kendall@entrywire.com"
        send_mail(subject, str(referral['email']), html, sender)
        referral_object = Referral(name=str(referral['name']), email=str(referral['email']), referred_by=student)
        referral_object.save()

@login_required
def google_login(request):
    client_id = os.environ['GOOGLE_CLIENT_ID']
    scope = 'https://www.googleapis.com/auth/contacts.readonly'
    state = str(uuid.uuid4())
    redirect_uri = '%s/oauth2callback/' % os.environ['PATH_URL']
    base_url = 'https://accounts.google.com/o/oauth2/auth?'
    params = {'scope':scope, 'state':state, 'client_id':client_id,
    'redirect_uri':redirect_uri, 'response_type':'code'}
    url = base_url + urllib.urlencode(params)
    return HttpResponseRedirect(url)

@login_required
@csrf_exempt
def referral_select(request, access_token):
    student = Student.objects.get(user=request.user)
    results = get_contacts(student, access_token)
    return render_to_response('referral_select.html', {'results':results, 'student':student}, 
        context_instance=RequestContext(request))

@login_required
def oauth2callback(request):
    code = request.GET['code']
    access_token = authenticate_google(code)
    url = reverse('referral_select', args=[access_token,])
    return HttpResponseRedirect(url) 

