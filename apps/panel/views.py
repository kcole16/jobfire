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
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from apps.panel.forms import UniversityForm
from apps.profile.models import *

logger = logging.getLogger("error.logger")

@staff_member_required
def create_university(request):
    if request.POST:
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UniversityForm()
    return render_to_response('create_university.html',
                              {'form': form},
                              context_instance=RequestContext(request))