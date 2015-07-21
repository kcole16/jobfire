from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'apps.profile.views.home', name='home'),    
    #Login
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', 'apps.profile.views.logout_view', name='logout'),
    url(r'^student_signup/', 'apps.profile.views.student_signup', name='student_signup'),
    # url(r'^recruiter_signup', 'apps.profile.views.recruiter_signup', name='recruiter_signup'),

    #Apply
    url(r'^apply/(.+)/', 'apps.profile.views.apply', name='apply'),

    #Privacy and Terms
    url(r'^privacy/', 'apps.profile.views.privacy', name='privacy'),
    url(r'^about/', 'apps.profile.views.about', name='about'),
    url(r'^terms/', 'apps.profile.views.terms', name='terms'),

)
