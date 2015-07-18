from django import forms


class CandidateForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.CharField(label="Email")
    website = forms.CharField(required=False, initial="None")
    github = forms.CharField(required=False, initial="None")
    desired_role = forms.CharField(label="Specialty")
    location = forms.CharField(label="Location")
    second_location = forms.CharField(required=False, initial="None")
    college = forms.CharField(label="University")
    resume = forms.FileField()

    def clean(self):
        cleaned_data = super(CandidateForm, self).clean()
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