from django import forms
from apps.profile.models import University

class RecommendationForm(forms.Form):
    class Meta:
        model = University
        fields = '__all__'

class RecommendationForm(forms.Form):
    posting = forms.CharField()