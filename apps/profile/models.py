from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class University(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=500)
	logo = models.FileField(upload_to="university/logos")
	color_main = models.CharField(max_length=10)
	color_secondary = models.CharField(max_length=10)

class Industry(models.Model):
	name = models.CharField(max_length=500)

class Major(models.Model):
	name = models.CharField(max_length=100)

class Student(models.Model):
	user = models.ForeignKey(User)
	first_name = models.CharField(max_length=500)
	last_name = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	major = models.ForeignKey(Major)
	industries = models.ManyToManyField(Industry)
	university = models.ForeignKey(University)
	resume_s3 = models.CharField(max_length=1000)

class Company(models.Model):
	name = models.CharField(max_length=500)
	logo = models.CharField(max_length=500)
	about = models.CharField(max_length=1000)
	url = models.CharField(max_length=500)
	address = models.CharField(max_length=500)
	industry = models.ForeignKey(Industry)
	universities = models.ManyToManyField(University)
	phone = models.CharField(max_length=16)

class Recruiter(models.Model):
	user = models.ForeignKey(User)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	company = models.ForeignKey(Company)

class Posting(models.Model):
	date_created = models.DateField(auto_now_add=True)
	expiration_date = models.DateField()
	job_start_date = models.CharField(max_length=100)
	position = models.CharField(max_length=100)
	role = models.CharField(max_length=100)
	job_type = models.CharField(max_length=100)
	company = models.ForeignKey(Company)
	location = models.CharField(max_length=100)
	university = models.ForeignKey(University)
	active = models.BooleanField(default=True)
	description = models.TextField()

class Application(models.Model):
	posting = models.ForeignKey(Posting)
	student = models.ForeignKey(Student)
	company = models.ForeignKey(Company)
	interview_granted = models.NullBooleanField(default=None)

class Interview(models.Model):
	date = models.DateField()
	application = models.ForeignKey(Application)
	posting = models.ForeignKey(Posting)
	student = models.ForeignKey(Student)
	company = models.ForeignKey(Company)

class Document(models.Model):
	type = models.CharField(max_length=100)
	s3_location = models.CharField(max_length=100)
	student = models.ForeignKey(Student)






