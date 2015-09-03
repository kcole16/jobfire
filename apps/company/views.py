from uuid import uuid4
import os
import urllib 
import datetime
import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, \
    redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from apps.company.forms import CompanyForm, PostingForm, UpdateForm, UpdatePasswordForm
from apps.profile.models import *
from apps.profile.utils import send_mail, send_conf_email, format_city
from apps.company.utils import add_to_algolia

import bugsnag
from mixpanel import Mixpanel
from algoliasearch import algoliasearch
from bugsnag.handlers import BugsnagHandler


logger = logging.getLogger("error.logger")

@login_required
def company_home(request):
    company = Recruiter.objects.get(user=request.user).company
    postings = Posting.objects.filter(company=company)
    count = 0
    list_num = 0
    posting_list = [[]]
    for posting in postings:
        if count < 3:
            posting_list[list_num].append(posting)
            count += 1
        else:
            count = 1
            list_num += 1
            posting_list.append([posting])

    return render_to_response('company_home.html', {'posting_list':posting_list, 'company':company}, 
        context_instance=RequestContext(request))

def company_signup(request):
    if request.POST:
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                logo = request.FILES['logo'].read()
            except MultiValueDictKeyError:
                logo = "Ask"
            uuid = uuid4()
            s3 = default_storage.open('jobfire/company_logos/%s' % uuid, 'w')
            s3.write(logo)
            s3.close()
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(email, email, 'password')
            except IntegrityError:
                message = 'An account already exists for this email address'
                return render_to_response('company_signup.html', {'form':form, 'message':message}, context_instance=RequestContext(request))
            user.set_password(form.cleaned_data['password'])
            user.save()
            industry = Industry.objects.get(name="Technology")
            company = Company(name=form.cleaned_data['name'],
                                logo="https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/jobfire/company_logos/%s" % uuid,
                                about=form.cleaned_data['about'],
                                url=form.cleaned_data['url'],
                                address=form.cleaned_data['address'],
                                phone=form.cleaned_data['phone'],
                                industry=industry
                                )
            company.save()
            recruiter = Recruiter(user=user, first_name=company, last_name=company, 
                email=form.cleaned_data['email'], company=company)
            recruiter.save()
            current_user = authenticate(username=recruiter.email,
                                        password=form.cleaned_data['password'])
            login(request, current_user)
            return redirect('company_home')
        else:
            logger.error(form.errors)
    else:
        form = CompanyForm()
    return render_to_response('company_signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def create_posting(request):
    company = Recruiter.objects.get(user=request.user).company
    universities = University.objects.all()
    if request.POST:
        form = PostingForm(request.POST)
        if form.is_valid():
            universities = request.POST['universities'].split(',')
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=90)
            posting = Posting(expiration_date=expiration_date,
                                job_start_date=form.cleaned_data['job_start_date'],
                                position=form.cleaned_data['position'],
                                job_type=form.cleaned_data['job_type'],
                                company=company,
                                role=form.cleaned_data['role'],
                                location=form.cleaned_data['location'],
                                university=University.objects.get(pk=universities[0]),
                                description=form.cleaned_data['description']
                                )
            posting.save()
            for university in universities:
                new_posting = UniversityPosting(posting=posting, university=University.objects.get(pk=university))
                print new_posting
                new_posting.save()
            return redirect('home')
    else:
        form = PostingForm()
    return render_to_response('create_posting.html',
                              {'form': form, 'company':company, 'universities':universities},
                              context_instance=RequestContext(request))

@login_required
def update_posting(request, posting_id):
    posting = Posting.objects.get(pk=posting_id)
    company = posting.company
    universities = University.objects.all()
    preselected = UniversityPosting.objects.filter(posting=posting).values_list('university_id', flat=True)
    print preselected
    if request.POST:
        form = PostingForm(request.POST, instance=posting)
        if form.is_valid():
            universities = request.POST['universities'].split(',')
            form.save()
            for university in universities:
                new_posting = UniversityPosting(posting=posting, university=University.objects.get(pk=university))
                new_posting.save()
            return redirect('home')
    else:
        form = PostingForm(instance=posting)
    return render_to_response('update_posting.html',
                              {'form': form, 'posting':posting, 'company':company,
                              'universities':universities, 'preselected':preselected},
                              context_instance=RequestContext(request))

@login_required
def view_posting(request, posting_id):
    company = Recruiter.objects.get(user=request.user).company
    posting = Posting.objects.get(pk=posting_id)
    return render_to_response('view_posting.html', 
        {'posting':posting, 'company':company}, context_instance=RequestContext(request))

@login_required
def remove_posting(request, posting_id):
    company = Recruiter.objects.get(user=request.user).company
    posting = Posting.objects.get(pk=posting_id)
    if company.id == posting.company.id:
    	posting.delete()
	return redirect('company_home')

@login_required
def company_profile(request):
	recruiter = Recruiter.objects.get(user=request.user)
	company = recruiter.company
	return render_to_response('company_profile.html', 
        {'recruiter':recruiter, 'company':company}, context_instance=RequestContext(request))

@login_required
def update_company_profile(request):
    recruiter = Recruiter.objects.get(user=request.user)
    company = recruiter.company
    if request.POST:
        form = UpdateForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            if form.cleaned_data['logo']:
                logo = request.FILES['logo'].read()
                uuid = uuid4()
            	s3 = default_storage.open('jobfire/company_logos/%s' % uuid, 'w')
                s3.write(logo)
                s3.close()
                company.logo="https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/jobfire/company_logos/%s" % uuid
            if str(form.cleaned_data['email']) != str(recruiter.email):
            	user = request.user
            	new_email = form.cleaned_data['email']
            	recruiter.email = new_email
            	recruiter.save()
            	user.email = new_email
            	user.username = new_email
            	user.save()
            company.save()
            return redirect('company_profile')
        else:
            print form.errors
    else:
        form = UpdateForm(instance=company)
    return render_to_response('update_company_profile.html',
                              {'form': form, 'company':company, 'recruiter':recruiter},
                              context_instance=RequestContext(request))

@login_required
def change_password(request):
    company = Recruiter.objects.get(user=request.user).company
    if request.POST:
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            return redirect('company_profile')
        else:
            print form.errors
    else:
        form = UpdatePasswordForm()
    return render_to_response('change_password.html',
                              {'form': form, 'company':company},
                              context_instance=RequestContext(request))

def all_applicants(request):
    company = Recruiter.objects.get(user=request.user).company
    applications = Application.objects.filter(company=company)
    return render_to_response('all_applicants.html', {'company':company, 'applications':applications})

def view_student(request, student_id):
    company = Recruiter.objects.get(user=request.user).company
    student = Student.objects.get(pk=student_id)
    return render_to_response('view_student.html',
                              {'student': student, 'company':company},
                              context_instance=RequestContext(request))

# def confirm_email(request, email_token):
#     success = False
#     try:
#         email_conf = EmailConfirmation.objects.get(code=email_token)
#     except ObjectDoesNotExist:
#         pass
#     else:
#         student = Student.objects.get(user=email_conf.user)
#         student.confirmed = True
#         student.save()
#         success = True
#     return render_to_response('confirm_email.html', {'success':success}, context_instance=RequestContext(request))

