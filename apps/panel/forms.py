from django import forms
from apps.profile.models import University

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = '__all__'