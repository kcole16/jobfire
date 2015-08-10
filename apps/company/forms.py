from django import forms
from apps.profile.models import Posting, Company
from tinymce.widgets import TinyMCE
from apps.profile.utils import format_city


class CompanyForm(forms.Form):
    name = forms.CharField(label="Name")
    logo = forms.FileField()
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password")
    about = forms.CharField(label="About")
    url = forms.CharField(label="URL")
    address = forms.CharField(label="Address")
    phone = forms.CharField(label="Phone")

class UpdateForm(forms.ModelForm):
    logo = forms.FileField(required=False)
    password = forms.CharField(required=False)
    email = forms.CharField(required=False)

    class Meta:
        model = Company
        fields = ['name','about','url','address','phone']
        widgets = {
            'about': forms.Textarea(attrs={'class': 'materialize-textarea'})
        }

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