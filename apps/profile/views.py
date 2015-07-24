from uuid import uuid4
import os
import urllib 

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
from apps.profile.forms import StudentForm, PostingForm
from apps.profile.models import *
from apps.profile.utils import add_to_algolia

import bugsnag
from algoliasearch import algoliasearch

def home(request):
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
    except ObjectDoesNotExist:
        applications = []
    else:
        apps = Application.objects.filter(student=student)
        applications = [app.posting.id for app in apps]
    return render_to_response('index.html', {'postings':postings, 'count':count, 
        'applications':applications,'context_list':context_list}, context_instance=RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html')

def terms(request):
    return render_to_response('terms.html')

def about(request):
    return render_to_response('about.html')

def posting_detail(request, posting_id):
    posting = Posting.objects.get(pk=posting_id)
    return render_to_response('posting_detail.html', 
        {'posting':posting}, context_instance=RequestContext(request))

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
        form.is_valid()
        try:
            resume = request.FILES['resume'].read()
        except MultiValueDictKeyError:
            resume = "Ask"
        uuid = uuid4()
        s3 = default_storage.open('jobfire/resumes/%s' % uuid, 'w')
        s3.write(resume)
        s3.close()
        email = form.cleaned_data['email']
        user = User.objects.create_user(email, email, 'password')
        user.set_password(form.cleaned_data['password'])
        user.save()
        major = Major.objects.get(name=form.cleaned_data['major'])
        university = University.objects.get(name=form.cleaned_data['university'])
        industry = Industry.objects.get(name="Finance")
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
        return redirect('home')
    else:
        form = StudentForm()
        universities = University.objects.all()
        industries = Industry.objects.all()
        majors = Major.objects.all()
    return render_to_response('student_signup.html',
                              {'form': form, 'universities':universities,
                              'industries':industries, 'majors':majors},
                              context_instance=RequestContext(request))

@login_required
def create_posting(request):
    if request.POST:
        form = PostingForm(request.POST)
        form.is_valid()
        company = Company.objects.get(name=form.cleaned_data['company'])
        university = University.objects.get(name='University of Virginia')
        posting = Posting(expiration_date='2015-12-31',
                            position=form.cleaned_data['position'],
                            job_type=form.cleaned_data['job_type'],
                            company=company,
                            location=form.cleaned_data['location'],
                            university=university,
                            description=form.cleaned_data['description']
                            )
        posting.save()
        add_to_algolia(posting)
        return redirect('home')
    else:
        form = PostingForm()
        universities = University.objects.all()
        companies = Company.objects.all()
    return render_to_response('create_posting.html',
                              {'form': form, 'universities':universities,
                              'companies':companies},
                              context_instance=RequestContext(request))

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

