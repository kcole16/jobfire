from django import forms
from apps.profile.models import Posting, Student
from tinymce.widgets import TinyMCE
from apps.profile.utils import format_city


class StudentForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(label="Password")
    email = forms.CharField(label="Email")
    major = forms.CharField(label="Major")
    grad_year = forms.CharField(label="Graduation Date")
    semester = forms.CharField()
    resume = forms.FileField(required=False)

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data


class StudentUpdateForm(forms.ModelForm):
    resume = forms.FileField(required=False)
    semester = forms.CharField(required=False)
    grad_year = forms.CharField(required=False)
    class Meta:
        model = Student
        fields = ['first_name','last_name','major', 'linkedin', 'portfolio']

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['portfolio'].required = False
        self.fields['linkedin'].required = False
        self.fields['major'].required = False


class CompanyForm(forms.Form):
    name = forms.CharField(label="Name")
    logo = forms.FileField()
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")
    about = forms.CharField(label="About")
    url = forms.CharField(label="URL")
    address = forms.CharField(label="Address")
    phone = forms.CharField(label="Phone")

class QuickSignupForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")


class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = ['job_start_date', 'university', 'position', 'role', 
        'job_type', 'location', 'description']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30, 'placeholder':'Description'}),
            'location': forms.TextInput(attrs={'id':'pac-input', 'placeholder': 'Washington, DC'}),
            'position': forms.TextInput(attrs={'placeholder': 'Software Engineer'})
        }
    def clean_location(self):
            location = format_city(self.cleaned_data['location'])

            return location 
            
class UpdatePasswordForm(forms.Form):
    password = forms.CharField(label="Password")
