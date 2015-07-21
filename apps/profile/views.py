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
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from apps.profile.forms import StudentForm
from apps.profile.models import *

import bugsnag
from algoliasearch import algoliasearch

@login_required
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
    else:
        postings = index.search(query)['hits']
    return render_to_response('index.html', {'postings':postings, 'context_list':context_list}, context_instance=RequestContext(request))

def privacy(request):
    return render_to_response('privacy.html')

def terms(request):
    return render_to_response('terms.html')

def about(request):
    return render_to_response('about.html')

def apply(request, posting_id):
    posting = Posting.objects.get(pk=posting_id)
    return render_to_response('apply.html', 
        {'posting':posting}, context_instance=RequestContext(request))

def student_signup(request):
    if request.POST:
        form = StudentForm(request.POST, request.FILES)
        form.is_valid()
        try:
            resume = request.FILES['resume'].read()
        except MultiValueDictKeyError:
            resume = "Ask"
        uuid = uuid4()
        # s3 = default_storage.open('resumes/%s' % uuid, 'w')
        # s3.write(resume)
        # s3.close()
        email = form.cleaned_data['email']
        user = User.objects.create_user(email, email, 'password')
        user.set_password(form.cleaned_data['password'])
        user.save()
        major = Major.objects.get(name=form.cleaned_data['major'])
        university = University.objects.get(name=form.cleaned_data['university'])
        industry = Industry.objects.get(name=form.cleaned_data['industries'])
        student = Student(user=user,
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            major=major,
                            university=university,
                            resume_s3="https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/resumes/%s" % uuid
                            )
        student.save()
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

def create_posting(request):
    if request.POST:
        form = StudentForm(request.POST, request.FILES)
        form.is_valid()
        try:
            resume = request.FILES['resume'].read()
        except MultiValueDictKeyError:
            resume = "Ask"
        uuid = uuid4()
        # s3 = default_storage.open('resumes/%s' % uuid, 'w')
        # s3.write(resume)
        # s3.close()
        email = form.cleaned_data['email']
        user = User.objects.create_user(email, email, 'password')
        user.set_password(form.cleaned_data['password'])
        user.save()
        major = Major.objects.get(name=form.cleaned_data['major'])
        university = University.objects.get(name=form.cleaned_data['university'])
        industry = Industry.objects.get(name=form.cleaned_data['industries'])
        student = Student(user=user,
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            email=form.cleaned_data['email'],
                            major=major,
                            university=university,
                            resume_s3="https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/resumes/%s" % uuid
                            )
        student.save()
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
def logout_view(request):
    logout(request)
    return redirect('login')

