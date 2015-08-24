from django.db import models

from apps.profile.models import Student

class Referral(models.Model):
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	referred_by = models.ForeignKey(Student)

# Create your models here.
