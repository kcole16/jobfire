import os
import time
import logging
import json

from apps.profile.models import Student, University
from django.core.exceptions import ObjectDoesNotExist

import requests
from algoliasearch import algoliasearch
from bs4 import BeautifulSoup

logger = logging.getLogger("error.logger")

COMMAND_LIST = """Sorry, that is not a valid command. Try one of these:
User Count: <University Name>
Total User Count
"""

def clean_text(text):
	if "<@U09SD8QG6>" in text:
		try:
			command = text.split(":")[1].strip()
			body = text.split(":")[2].strip()
		except IndexError:
			command = text.split(":")[1].strip()
			body = None
	else:
		if ":" in text:
			command = text.split(":")[0].strip()
			body = text.split(":")[1].strip()
		else:
			command = text
			body = None

	return command, body

def handle_command(text):
	command, body = clean_text(text)
	if command == "User Count":
		message = user_count_uni(body)
	elif command == "Total User Count":
		message = total_user_count()
	else:
		message = COMMAND_LIST
	return message

def user_count_uni(body):
	try:
		university = University.objects.get(name=body)
	except ObjectDoesNotExist:
		message = "University does not exist"
	else:
		student_count = Student.objects.filter(university=university).count()
		message = "There are %d students signed up from %s" % (student_count, university.name)
	return message

def total_user_count():
	students = Student.objects.all().count()
	message = "There are %d total students" % students
	return message

def slackbot(data):
	for request in data:
		message = handle_command(request['text'])
		return message


