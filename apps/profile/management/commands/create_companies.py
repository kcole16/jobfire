import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from apps.profile.models import *
from apps.profile.utils import connect_db
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

def try_attribute(attribute, company):
    if attribute == 'locations':
        try:
            attribute = company['locations'][0]['display_name']
        except (KeyError, IndexError):
            attribute = 'None'
        return attribute
    try:
        attribute = company[attribute]
    except KeyError:
        attribute="None"
    if attribute is None:
        attribute = "None"
    return attribute


def create_companies():
    db = connect_db()
    companies = db.companies.find()
    for company in companies:
        try:
            c = Company.objects.get(name=company['name'])
        except ObjectDoesNotExist:
            url = company['company_url']
            if url is None:
                url = "None"
            if 'www' in url:
                base_url = url.split('www.')[1]
            elif 'http' in url:
                base_url = url.split('//')[1]
            else:
                try:
                    base_url = url.split('.')[1]
                except IndexError:
                    base_url = None
            email = ("temp@%s" % base_url).strip('/')
            try:
                user = User(username=email, email=email, password="temp123")
                user.save()
            except:
                pass
            else:
                industry = Industry.objects.get(name="Technology")
                company = Company(
                    name=try_attribute('name', company),
                    logo=try_attribute('logo_url', company),
                    about=try_attribute('product_desc', company),
                    url=try_attribute('company_url', company),
                    address=try_attribute('locations', company),
                    industry=industry,
                    phone="8888888888"
                    )
                company.save()
                recruiter = Recruiter(user=user,
                    first_name=company.name,
                    last_name=company.name,
                    email=email,
                    company=company)
                recruiter.save()
                print email
        else:
            pass


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_companies()