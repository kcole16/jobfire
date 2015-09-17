import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from apps.profile.models import *
from apps.profile.utils import connect_db
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

import pymongo

def try_attribute(attribute, data):
    try:
        value = data[attribute]
    except KeyError:
        value = None
    if attribute != 'funding_stage':
        if value == '' or value == None or value == 'Undisclosed':
            value = 0
    return value

def get_data():
    db = connect_db()
    companies = Company.objects.all()
    for company in companies:
        data = db.companies.find_one({"name":company.name})
        if data:
            company.total_funding = int(try_attribute('total_funding', data))
            company.funding_stage = try_attribute('funding_stage', data)
            company.growth = int(try_attribute('growth', data))
            company.hype = int(try_attribute('mindshare', data))
            company.employees = int(try_attribute('employees', data))
            company.save()
            print company.name

class Command(BaseCommand):

    def handle(self, *args, **options):
        get_data()