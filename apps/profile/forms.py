from django import forms
from apps.profile.models import Posting
from tinymce.widgets import TinyMCE


class StudentForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(label="Password")
    email = forms.CharField(label="Email")
    major = forms.CharField(label="Major")
    resume = forms.FileField()

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data


class CompanyForm(forms.Form):
    name = forms.CharField(label="Name")
    logo = forms.FileField()
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")
    about = forms.CharField(label="About")
    url = forms.CharField(label="URL")
    address = forms.CharField(label="Address")
    phone = forms.CharField(label="Phone")


class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = ['job_start_date', 'university', 'position', 'role', 
        'job_type', 'location', 'description']
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30, 'placeholder':'Description'}),
            'university': forms.Select(choices=(('this','that'),))
        }
