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
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.profile.forms import StudentForm, CompanyForm, PostingForm, StudentUpdateForm, UpdatePasswordForm, QuickSignupForm
from apps.profile.models import *
from apps.profile.utils import *

import bugsnag
from mixpanel import Mixpanel
from algoliasearch import algoliasearch
from bugsnag.handlers import BugsnagHandler


logger = logging.getLogger("error.logger")

def home(request):
    error = None
    if request.user.is_authenticated():
        try:
            recruiter = Recruiter.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return redirect('student_home')
        else:
            return redirect('company_home')
    else:
        if request.POST:
            form = QuickSignupForm(request.POST)
            if form.is_valid():
                mp = Mixpanel(os.environ['MIXPANEL_TOKEN'])
                email = str(form.cleaned_data['email'])
                try:
                    root = email.split('@')[1].split(".")[-2:]
                    extension = "%s.%s" % (root[0], root[1])
                except IndexError:
                    error = "Please enter a valid email address"
                    form = QuickSignupForm()
                    return render_to_response('index.html', {'error':error, 'form':form}, 
                        context_instance=RequestContext(request))
                try: 
                    university = University.objects.get(email_ext=extension)
                except ObjectDoesNotExist:
                    mp.track(email, 'Attempted Signup: Unsupported School', {
                        'Email': email,
                        'Extension': extension
                    })
                    return render_to_response('sorry.html')
                else:
                    try:
                        user = User.objects.create_user(email, email, 'password')
                    except IntegrityError:
                        message = 'An account already exists for this email address'
                        return render_to_response('student_signup.html', {'form':form, 'message':message}, context_instance=RequestContext(request))
                    user.set_password(form.cleaned_data['password'])
                    user.save()
                    student = Student(user=user,
                                        email=form.cleaned_data['email'],
                                        university=university,
                                        )
                    student.save()
                    email_token = str(uuid4()).replace('-', '')
                    email_conf = EmailConfirmation(user=user, code=email_token)
                    email_conf.save()
                    mp.people_set(student.id, {
                        '$email'         : student.email,
                        '$university'         : student.university.name,
                        '$type': 'student',
                        '$created': student.user.date_joined,
                        '$email_token': email_token
                    })
                    send_conf_email(student, email_token)
                    current_user = authenticate(username=email,
                                                password=form.cleaned_data['password'])
                    login(request, current_user)
                    return redirect('student_home')
        else:
            form = QuickSignupForm()
        return render_to_response('index.html', {'form':form, 'error':error}, context_instance=RequestContext(request))

@login_required
def student_home(request):
    student = Student.objects.get(user=request.user)
    markets = student.university.market_set.all()
    template = 'student_home.html'
    page_template = "_postings.html"
    # client = algoliasearch.Client("74PKG6FSJB", os.environ['ALGOLIA_KEY']);
    # index = client.init_index('Postings')
    args = request.GET.dict()
    page = request.GET.get('page')
    args.pop('page', None)
    args.pop('querystring_key', None)
    if 'q' in args.keys():
        q = str(args['q'].decode('utf-8'))
        o_q = q.title()
        args.pop('q')
        companies = Company.objects.filter(Q(about__contains=o_q) | Q(about__contains=q) | Q(name__contains=o_q) | Q(name__contains=q))
        if companies.count() > 1:
            company_ids = [company.id for company in companies]
        elif companies.count() == 1:
            company_ids = [companies[0].id]
        else:
            company_ids = []
        first_results = Posting.objects.filter(**args).order_by('company').order_by('-priority')
        postings_list = []
        for result in first_results:
            if q in result.description or o_q in result.description or result.company.id in company_ids:
                postings_list.append(result)
        # for k in args:
        #     query += " %s" % str(args[k].decode('utf-8'))
        #     context_list.append(args[k])
        # results = index.search(query)['hits']
        # postings_list = []
        # for result in results:
        #     for k in args:
        #         if result[k] == args[k]:
        #             postings_list.append(result)
        # count = len(postings_list)
        # postings_list = []
    else:
        postings_list = Posting.objects.filter(**args).order_by('company').order_by('-priority')
        # results = Posting.objects.raw('select * from profile_posting where id not in (select posting_id from profile_application where student_id = %s) and university_id = %s;' % (student.id, student.university.id))
        # for result in results:
        #     for k in args:

        #             postings_list.append(result)
    applications = Application.objects.filter(student=student).values_list('posting_id', flat=True).order_by('id')
    follows = Follow.objects.filter(student=student).values_list('posting_id', flat=True).order_by('id')

    #Only exists while pitching Start @ Startup, needs to exist for all
    # if student.university.name == 'Start @ a Startup':
    up = UniversityPosting.objects.filter(university=student.university).values_list('posting_id', flat=True).order_by('id')
    postings_list = [posting for posting in postings_list 
    if posting.id not in applications and posting.id not in follows and posting.id in up]
    # else:
    #     postings_list = [posting for posting in postings_list if posting.id not in applications]
    entries = postings_list
    count = len(entries)
    if request.is_ajax():
        template = "_postings.html"

    formatted_args = ""
    if args != {}:
        formatted_args = "&" + urllib.urlencode(args)

    return render_to_response(template, {'entries':entries, 'count':count, 'page_template':page_template, 
        'student':student, 'markets': markets, 
        'formatted_args':formatted_args}, context_instance=RequestContext(request))

@login_required
def posting_detail(request, posting_id):
    applied = False
    following = False
    student = Student.objects.get(user=request.user)
    posting = Posting.objects.get(pk=posting_id)
    try:
        application = Application.objects.get(student=student, posting=posting)
    except ObjectDoesNotExist:
        pass
    else:
        applied = True
    try:
        follow = Follow.objects.get(student=student, posting=posting)
    except ObjectDoesNotExist:
        pass
    else:
        following = True
    return render_to_response('posting_detail.html', 
        {'posting':posting, 'applied':applied, 'following':following, 
        'student':student}, context_instance=RequestContext(request))

@login_required
def apply(request, posting_id):
    student = Student.objects.get(user=request.user)
    posting = Posting.objects.get(id=posting_id)
    if student.resume_s3 == None or student.confirmed == False or posting.started == False:
        return redirect('home')
    try:
        application = Application.objects.get(student=student, posting=posting)
    except ObjectDoesNotExist: 
        application = Application(posting=posting, student=student, 
            company=posting.company)
        application.save()
        mp = Mixpanel(os.environ['MIXPANEL_TOKEN'])
        mp.track(student.id, 'Applied to Company', {
            'Company': posting.company.name,
        })
        mp.people_increment(student.id, {
            'Job Apps': 1
        })
    subject = "Successfully Applied to %s" % posting.company.name
    sender = "Kendall Cole at EntryWire <kendall@entrywire.com>"
    html = """<p>Hey %s,</p>
    <p>You've successfully applied to the %s position at %s! They've received your resume, and will be in touch with next steps.</p>
    <p>If you have any questions, feel free to contact me at kendall@entrywire.com.</p>
    <p>Best of luck,</p>
    <p>Kendall<br>Co-Founder<br>EntryWire, Inc.</p>""" % (student.first_name, posting.position, posting.company.name)
    send_mail(subject, student.email, html, sender)
    text = "%s %s from %s applied to the %s position at %s. Resume: %s" % (student.first_name, student.last_name,
        student.university.name, posting.position, posting.company.name, student.resume_s3)
    channel = "applications"
    slack_notification(channel, text)
    return redirect('applications')

@login_required
def follow(request, posting_id):
    student = Student.objects.get(user=request.user)
    posting = Posting.objects.get(id=posting_id)
    try:
        follow = Follow.objects.get(student=student, posting=posting)
    except ObjectDoesNotExist: 
        follow = Follow(posting=posting, student=student, 
            company=posting.company)
        follow.save()
        mp = Mixpanel(os.environ['MIXPANEL_TOKEN'])
        mp.track(student.id, 'Following Company', {
            'Company': posting.company.name,
        })
        mp.people_increment(student.id, {
            'Following': 1
        })
    subject = "You're Now Following %s" % posting.company.name
    sender = "Kendall Cole at EntryWire <kendall@entrywire.com>"
    html = """<p>Hey %s,</p>
    <p>You're now following the %s position at %s! We've let the hiring manager know you're interested, and they'll let you know when the application process starts!</p>
    <p>If you have any questions, feel free to contact me at kendall@entrywire.com.</p>
    <p>Best of luck,</p>
    <p>Kendall<br>Co-Founder<br>EntryWire, Inc.</p>""" % (student.first_name, posting.position, posting.company.name)
    send_mail(subject, student.email, html, sender)
    text = "%s %s from %s is following the %s position at %s. Resume: %s" % (student.first_name, student.last_name,
        student.university.name, posting.position, posting.company.name, student.resume_s3)
    channel = "follows"
    slack_notification(channel, text)
    return redirect('following')

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
        {'applications':applications, 'student':student}, context_instance=RequestContext(request))

@login_required
def following(request):
    student = Student.objects.get(user=request.user)
    follows = Follow.objects.filter(student=student)
    return render_to_response('following.html', 
        {'follows':follows, 'student':student}, context_instance=RequestContext(request))

def student_signup(request):
    if request.POST:
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            mp = Mixpanel(os.environ['MIXPANEL_TOKEN'])
            email = str(form.cleaned_data['email'])
            root = email.split('@')[1].split(".")[-2:]
            extension = "%s.%s" % (root[0], root[1])
            graduation_date = "%s %s" % (form.cleaned_data['semester'],
                form.cleaned_data['grad_year'])
            try: 
                university = University.objects.get(email_ext=extension)
            except ObjectDoesNotExist:
                mp.track(email, 'Attempted Signup: Unsupported School', {
                    'Email': email,
                    'Extension': extension,
                    'First Name': form.cleaned_data['first_name'],
                    'Last Name': form.cleaned_data['last_name'],
                    'Major': form.cleaned_data['major'],
                    'Graduation Date': graduation_date
                })
                return render_to_response('sorry.html')
            else:
                resume_s3 = None
                if form.cleaned_data['resume']:
                    uuid = uuid4()
                    resume = request.FILES['resume'].read()
                    s3 = default_storage.open('jobfire/resumes/%s' % uuid, 'w')
                    s3.write(resume)
                    s3.close()
                    resume_s3 = "https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/jobfire/resumes/%s" % uuid
                try:
                    user = User.objects.create_user(email, email, 'password')
                except IntegrityError:
                    message = 'An account already exists for this email address'
                    return render_to_response('student_signup.html', {'form':form, 'message':message}, context_instance=RequestContext(request))
                user.set_password(form.cleaned_data['password'])
                user.save()
                major = Major.objects.get(name=form.cleaned_data['major'])
                industry = Industry.objects.get(name="Technology")
                student = Student(user=user,
                                    first_name=form.cleaned_data['first_name'],
                                    last_name=form.cleaned_data['last_name'],
                                    email=form.cleaned_data['email'],
                                    major=major,
                                    university=university,
                                    graduation_date=graduation_date,
                                    resume_s3=resume_s3
                                    )
                student.save()
                email_token = str(uuid4()).replace('-', '')
                email_conf = EmailConfirmation(user=user, code=email_token)
                email_conf.save()
                mp.people_set(student.id, {
                    '$first_name'    : student.first_name,
                    '$last_name'     : student.last_name,
                    '$email'         : student.email,
                    '$university'         : student.university.name,
                    '$major' : student.major.name,
                    '$type': 'student',
                    '$created': student.user.date_joined,
                    '$email_token': email_token
                })
                send_conf_email(student, email_token)
                current_user = authenticate(username=email,
                                            password=form.cleaned_data['password'])
                login(request, current_user)
                return redirect('student_home')  
        else:
            logger.error(form.errors)
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
def update_profile(request):
    student = Student.objects.get(user=request.user)
    semester = None
    grad_year = None
    if request.POST:
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            mp = Mixpanel(os.environ['MIXPANEL_TOKEN'])
            major = "None"
            if form.cleaned_data['major']:
                major = Major.objects.get(name=form.cleaned_data['major']).name
            form.save()
            student.graduation_date = "%s %s" % (form.cleaned_data['semester'],
                form.cleaned_data['grad_year'])
            if form.cleaned_data['resume']:
                resume = request.FILES['resume'].read()
                uuid = uuid4()
                s3 = default_storage.open('jobfire/resumes/%s' % uuid, 'w')
                s3.write(resume)
                s3.close()
                student.resume_s3="https://s3.amazonaws.com/elasticbeanstalk-us-east-1-745309683664/jobfire/resumes/%s" % uuid
            student.save()
            mp.people_set(student.id, {
                '$first_name'    : student.first_name,
                '$last_name'     : student.last_name,
                '$email'         : student.email,
                '$university'         : student.university.name,
                '$major' : major
            })
            return redirect('student_profile')
        else:
            print form.errors
    else:
        form = StudentUpdateForm(instance=student)
        try:
            grad_info = student.graduation_date.split(' ')
        except AttributeError:
            semester = None
            grad_year = ""
        else:
            semester = grad_info[0]
            grad_year = grad_info[1]
    return render_to_response('update_profile.html',
                              {'form': form, 'semester':semester, 'grad_year':grad_year,
                              'student':student},
                              context_instance=RequestContext(request))

@login_required
def recommendations(request):
    student = Student.objects.get(user=request.user)
    recs = Recommendation.objects.filter(student=student)
    return render_to_response('recommendations.html', {'recs':recs, 'student':student},
        context_instance=RequestContext(request))

@login_required
def update_password(request):
    student = Student.objects.get(user=request.user)
    if request.POST:
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            return redirect('student_profile')
        else:
            print form.errors
    else:
        form = UpdatePasswordForm()
    return render_to_response('update_password.html',
                              {'form': form, 'student':student},
                              context_instance=RequestContext(request))

def confirm_email(request, email_token):
    success = False
    try:
        email_conf = EmailConfirmation.objects.get(code=email_token)
    except ObjectDoesNotExist:
        pass
    else:
        student = Student.objects.get(user=email_conf.user)
        student.confirmed = True
        student.save()
        success = True
    return render_to_response('confirm_email.html', {'success':success}, context_instance=RequestContext(request))

@login_required
def get_linkedin(request):
    client_id = os.environ['LINKEDIN_CLIENT_ID']
    scope = 'r_basicprofile r_emailaddress'
    state = str(uuid4()).replace('-','')
    redirect_uri = '%s/oauth/' % str(os.environ['PATH_URL'])
    url = 'https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=%s&scope=%s&state=%s&redirect_uri=%s' % (client_id, scope, state, redirect_uri)
    return redirect(url)

@login_required
def oauth(request):
    code = request.GET['code']
    access_token = authenticate_linkedin(code)
    student = Student.objects.get(user=request.user)
    user_status = save_linkedin_profile(student, access_token)
    return redirect('student_profile')

@login_required
def company_detail(request, company_id):
    student = Student.objects.get(user=request.user)
    company = Company.objects.get(pk=company_id)
    postings = Posting.objects.filter(company=company)
    company_info = get_company_info(company.name)
    try:
        twitter = company_info['twitter_url'].split('.com/')[1]
    except:
        twitter = None
    return render_to_response('company_detail.html', {'company_info':company_info,
        'postings':postings, 'student':student, 'twitter':twitter},context_instance=RequestContext(request))

# @login_required
# def interviews(request):
#     student = Student.objects.get(user=request.user)
#     interviews = Interview.objects.filter(student=student)
#     return render_to_response('interviews.html', 
#         {'interviews':interviews}, context_instance=RequestContext(request))

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

