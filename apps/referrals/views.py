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

from datetime import datetime

import os
import uuid
import urllib
import requests
from bs4 import BeautifulSoup

def authenticate_google(code):
    url = 'https://www.googleapis.com/oauth2/v3/token'
    client_id = os.environ['GOOGLE_CLIENT_ID']
    client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': 'http://localhost:8000/oauth2callback/',
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
	for entry in entries:
		name = entry.find('title').string
		email = entry.find('gd:email')['address']
		if email.split('@')[1] == student.university.email_ext and name != None:
			results.append({'name':name, 'email':email})
	return results

@login_required
def google_login(request):
	client_id = os.environ['GOOGLE_CLIENT_ID']
	scope = 'https://www.googleapis.com/auth/contacts.readonly'
	state = str(uuid.uuid4())
	redirect_uri = 'http://localhost:8000/oauth2callback/'
	base_url = 'https://accounts.google.com/o/oauth2/auth?'
	params = {'scope':scope, 'state':state, 'client_id':client_id,
	'redirect_uri':redirect_uri, 'response_type':'code'}
	url = base_url + urllib.urlencode(params)
	return HttpResponseRedirect(url)

@login_required
def oauth2callback(request):
	code = request.GET['code']
	access_token = authenticate_google(code)
	student = Student.objects.get(user=request.user)
	results = get_contacts(student, access_token)
	return render_to_response('referral_select.html', {'results':results, 'student':student}, 
		context_instance=RequestContext(request))




