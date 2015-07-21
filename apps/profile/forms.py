from django import forms


class StudentForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(label="Password")
    email = forms.CharField(label="Email")
    university = forms.CharField(label="University")
    major = forms.CharField(label="Major")
    industries = forms.CharField(label="Industries")
    resume = forms.FileField()

    def clean(self):
        cleaned_data = super(StudentForm, self).clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data

class CompanyForm(forms.Form):
    name = forms.CharField(label="Company Name")
    website = forms.CharField(label="Site URL")
    contact_email = forms.CharField(label="Contact Email")
    contact_first_name = forms.CharField(label="First Name")
    contact_last_name = forms.CharField(label="Last Name")
    location = forms.CharField(label="Location")
    phone = forms.CharField(label="Phone Number")