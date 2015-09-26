from django.contrib import admin
from apps.profile.models import Posting, Company, University, Recommendation, UniversityPosting

admin.site.register(Posting)
admin.site.register(Company)
admin.site.register(University)
admin.site.register(UniversityPosting)
admin.site.register(Recommendation)

# Register your models here.
