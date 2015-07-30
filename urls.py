from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^$', 'apps.profile.views.home', name='home'),  
      
    #Login
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', 'apps.profile.views.logout_view', name='logout'),

    #Students
    url(r'^main/', 'apps.profile.views.student_home', name='student_home'),
    url(r'^student_signup/', 'apps.profile.views.student_signup', name='student_signup'),
    url(r'^posting_detail/(.+)/', 'apps.profile.views.posting_detail', name='posting_detail'),
    url(r'^apply/(.+)/', 'apps.profile.views.apply', name='apply'),
    url(r'^applications/', 'apps.profile.views.applications', name='applications'),
    url(r'^interviews/', 'apps.profile.views.interviews', name='interviews'),
    url(r'^student_profile/', 'apps.profile.views.student_profile', name='student_profile'),

    #Companies
    url(r'^company_signup/', 'apps.profile.views.company_signup', name='company_signup'),
    url(r'^dashboard/', 'apps.profile.views.company_home', name='company_home'),
    url(r'^create_posting/', 'apps.profile.views.create_posting', name='create_posting'),
    url(r'^view_posting/(.+)/', 'apps.profile.views.view_posting', name='view_posting'),
    url(r'^company_applications/', 'apps.profile.views.company_applications', name='company_applications'),

    #Privacy and Terms
    url(r'^privacy/', 'apps.profile.views.privacy', name='privacy'),
    url(r'^about/', 'apps.profile.views.about', name='about'),
    url(r'^terms/', 'apps.profile.views.terms', name='terms'),

)
