from uuid import uuid4
import os
import urllib 
import datetime
from ast import literal_eval

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
from apps.profile.forms import StudentForm, CompanyForm, PostingForm
from apps.profile.models import *
from apps.profile.utils import add_to_algolia

import bugsnag
from algoliasearch import algoliasearch


def home(request):
    if request.user.is_authenticated():
        try:
            recruiter = Recruiter.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('student_home')
        else:
            return redirect('company_home')
    else:
        return render_to_response('index.html')

@login_required
def student_home(request):
    client = algoliasearch.Client("E4AL29PC9K", os.environ['ALGOLIA_KEY']);
    index = client.init_index('Postings')
    context_list = []
    query = ""
    if request.GET.dict():
        args = request.GET.dict()
        for k in request.GET.dict():
            query += " %s" % str(args[k].decode('utf-8'))
            context_list.append(args[k])
        postings = index.search(query)['hits']
        count = len(postings)
    else:
        postings = Posting.objects.all()
        count = postings.count()
    try:
        student = Student.objects.get(user=request.user)
    except (ObjectDoesNotExist, TypeError):
        applications = []
        user = False
    else:
        apps = Application.objects.filter(student=student)
        applications = [app.posting.id for app in apps]
        user = True
    return render_to_response('student_home.html', {'postings':postings, 'count':count, 
        'applications':applications,'context_list':context_list, 'user':user}, context_instance=RequestContext(request))

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

    return render_to_response('company_home.html', {'posting_list':posting_list, 'company':company}, context_instance=RequestContext(request))

@login_required
def posting_detail(request, posting_id):
    posting = Posting.objects.get(pk=posting_id)
    return render_to_response('posting_detail.html', 
        {'posting':posting}, context_instance=RequestContext(request))

@login_required
def view_posting(request, posting_id):
    company = Recruiter.objects.get(user=request.user).company
    posting = Posting.objects.get(pk=posting_id)
    return render_to_response('view_posting.html', 
        {'posting':posting, 'company':company}, context_instance=RequestContext(request))

@login_required
def apply(request, posting_id):
    student = Student.objects.get(user=request.user)
    posting = Posting.objects.get(id=posting_id)
    application = Application(posting=posting, student=student, 
        company=posting.company)
    application.save()
    return redirect('applications')

@login_required
def student_profile(request):
    student = Student.objects.get(user=request.user)
    return render_to_response('student_profile.html', 
        {'student':student}, context_instance=RequestContext(request))

@login_required
def applications(request):
    student = Student.objects.get(user=request.user)
    applications = Application.objects.filter(student=student)
    return render_to_response('applications.html', 
        {'applications':applications}, context_instance=RequestContext(request))

@login_required
def interviews(request):
    student = Student.objects.get(user=request.user)
    interviews = Interview.objects.filter(student=student)
    return render_to_response('interviews.html', 
        {'interviews':interviews}, context_instance=RequestContext(request))

def student_signup(request):
    if request.POST:
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resume = request.FILES['resume'].read()
            except MultiValueDictKeyError:
                resume = "Ask"
            uuid = uuid4()
            s3 = default_storage.open('jobfire/resumes/%s' % uuid, 'w')
            s3.write(resume)
            s3.close()
            email = form.cleaned_data['email']
            try:
                user = User.objects.create_user(email, email, 'password')
            except IntegrityError:
                message = 'An account already exists for this email address'
                return render_to_response('student_signup.html', {'form':form, 'message':message}, context_instance=RequestContext(request))
            user.set_password(form.cleaned_data['password'])
            user.save()

            major = Major.objects.get(name=form.cleaned_data['major'])
            university = University.objects.get(name=form.cleaned_data['university'])
            industry = Industry.objects.get(name="Technology")
            student = Student(user=user,
                                first_name=form.cleaned_data['first_name'],
                                last_name=form.cleaned_data['last_name'],
                                email=form.cleaned_data['email'],
                                major=major,
                                university=university,
                                resume_s3="https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/jobfire/resumes/%s" % uuid
                                )
            student.save()
            current_user = authenticate(username=email,
                                        password=form.cleaned_data['password'])
            login(request, current_user)
            return redirect('student_home')  
        else:
            print form.errors
    else:     
        form = StudentForm()
        universities = University.objects.all()
        industries = Industry.objects.all()
        majors = Major.objects.all()
    return render_to_response('student_signup.html',
                              {'form': form, 'universities':universities,
                              'industries':industries, 'majors':majors},
                              context_instance=RequestContext(request))

def company_signup(request):
    if request.POST:
        form = CompanyForm(request.POST)
        form.is_valid()
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
        form = CompanyForm()
    return render_to_response('company_signup.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def create_posting(request):
    company = Recruiter.objects.get(user=request.user).company
    if request.POST:
        form = PostingForm(request.POST)
        form.is_valid()
        expiration_date = datetime.datetime.now() + datetime.timedelta(days=90)
        posting = Posting(expiration_date=expiration_date,
                            job_start_date=form.cleaned_data['job_start_date'],
                            position=form.cleaned_data['position'],
                            job_type=form.cleaned_data['job_type'],
                            company=company,
                            role=form.cleaned_data['role'],
                            location=form.cleaned_data['location'],
                            university=form.cleaned_data['university'],
                            description=form.cleaned_data['description']
                            )
        posting.save()
        # add_to_algolia(posting)
        return redirect('home')
    else:
        form = PostingForm()
    return render_to_response('create_posting.html',
                              {'form': form, 'company':company},
                              context_instance=RequestContext(request))

@login_required
def update_posting(request, posting_id):
    posting = Posting.objects.get(pk=posting_id)
    if request.POST:
        form = PostingForm(request.POST, instance=posting)
        if form.is_valid():
            form.save()
            return redirect('home')
        # add_to_algolia(posting)
    else:
        form = PostingForm(instance=posting)
    return render_to_response('update_posting.html',
                              {'form': form, 'posting':posting},
                              context_instance=RequestContext(request))

def company_applications(request):
    company = Recruiter.objects.get(user=request.user).company
    applications = Application.objects.filter(company=company)
    return render_to_response('company_applications.html', {'company':company})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def privacy(request):
    return render_to_response('privacy.html')

def terms(request):
    return render_to_response('terms.html')

def about(request):
    return render_to_response('about.html')

