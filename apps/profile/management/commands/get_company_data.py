import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from apps.profile.models import *
from apps.profile.utils import connect_db
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand


def get_data():
    db = connect_db()
    companies = Company.objects.all()
    for company in companies:
        data = db.companies.find_one({"name":company.name})
        if data:
            company.total_funding = int(data['total_funding'])
            company.funding_stage = data['funding_stage']
            company.growth = int(data['growth'])
            company.hype = int(data['mindshare'])
            company.employees = int(data['employees'])
            company.save
            print company.name

class Command(BaseCommand):

    def handle(self, *args, **options):
        get_data()