from django import forms
from apps.profile.models import University

class UniversityForm(forms.Form):
    class Meta:
        model = University
        fields = '__all__'

class RecommendationForm(forms.Form):
    posting = forms.CharField()