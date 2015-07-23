from django import forms


class StudentForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(label="Password")
    email = forms.CharField(label="Email")
    university = forms.CharField(label="University")
    major = forms.CharField(label="Major")
    resume = forms.FileField()

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data

class PostingForm(forms.Form):
    company = forms.CharField(label="Company")
    university = forms.CharField(label="University")
    position = forms.CharField(label="Position")
    job_type = forms.CharField(label="Job Type")
    location = forms.CharField(label="Location")
    description = forms.CharField(label="Description")
