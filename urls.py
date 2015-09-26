from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
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
    url(r'^follow/(.+)/', 'apps.profile.views.follow', name='follow'),
    url(r'^following/', 'apps.profile.views.following', name='following'),
    url(r'^recommendations/', 'apps.profile.views.recommendations', name='recommendations'),
    url(r'^student_profile/', 'apps.profile.views.student_profile', name='student_profile'),
    url(r'^update_profile/', 'apps.profile.views.update_profile', name='update_profile'),
    url(r'^confirm_email/(.+)/', 'apps.profile.views.confirm_email', name='confirm_email'),
    url(r'^update_password/', 'apps.profile.views.update_password', name='update_password'),
    url(r'^get_linkedin/', 'apps.profile.views.get_linkedin', name='get_linkedin'),
    url(r'^oauth/', 'apps.profile.views.oauth', name='oauth'),
    url(r'^company/(.+)/', 'apps.profile.views.company_detail', name='company_detail'),

    #Companies
    url(r'^company_signup/', 'apps.company.views.company_signup', name='company_signup'),
    url(r'^dashboard/', 'apps.company.views.company_home', name='company_home'),
    url(r'^create_posting/', 'apps.company.views.create_posting', name='create_posting'),
    url(r'^view_posting/(.+)/', 'apps.company.views.view_posting', name='view_posting'),
    url(r'^update_posting/(.+)/', 'apps.company.views.update_posting', name='update_posting'),
    url(r'^remove_posting/(.+)/', 'apps.company.views.remove_posting', name='remove_posting'),
    url(r'^all_applicants/', 'apps.company.views.all_applicants', name='all_applicants'),
    url(r'^view_student/(.+)/', 'apps.company.views.view_student', name='view_student'),
    url(r'^company_profile/', 'apps.company.views.company_profile', name='company_profile'),
    url(r'^update_company_profile/', 'apps.company.views.update_company_profile', name='update_company_profile'),
    url(r'^change_password/', 'apps.company.views.change_password', name='change_password'),

    #Referrals
    url(r'^invite_friends/', 'apps.referrals.views.google_login', name='invite_friends'),
    url(r'^oauth2callback/', 'apps.referrals.views.oauth2callback', name='oauth2callback'),
    url(r'^referral_select/(.+)/', 'apps.referrals.views.referral_select', name='referral_select'),
    url(r'^contact_referrals/', 'apps.referrals.views.contact_referrals', name='contact_referrals'),

    #Admin
    url(r'^panel/home/', 'apps.panel.views.panel_home', name='panel_home'),
    url(r'^panel/create_university/', 'apps.panel.views.create_university', name='create_university'),
    # url(r'^panel/create_recommendation/', 'apps.panel.views.create_recommendation', name='create_recommendation'),
    url(r'^panel/view_companies/', 'apps.panel.views.view_companies', name='view_companies'),
    url(r'^panel/view_universities/', 'apps.panel.views.view_universities', name='view_universities'),
    url(r'^panel/view_applicants/', 'apps.panel.views.view_applicants', name='view_applicants'),
    url(r'^panel/view_followers/', 'apps.panel.views.view_followers', name='view_followers'),
    url(r'^panel/view_students/(.+)/', 'apps.panel.views.view_students', name='view_students'),

    #Privacy and Terms
    url(r'^privacy/', 'apps.profile.views.privacy', name='privacy'),
    url(r'^about/', 'apps.profile.views.about', name='about'),
    url(r'^terms/', 'apps.profile.views.terms', name='terms'),

    #Dependencies
    (r'^tinymce/', include('tinymce.urls')),
    (r'^password_reset/', include('password_reset.urls')),

)
