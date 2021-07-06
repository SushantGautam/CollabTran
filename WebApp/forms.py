from django import forms
from django.contrib.auth.models import User

from . import models



class ContributionForm(forms.ModelForm):
    class Meta:
        model = models.Contribution
        fields = ['User']

class UrlsForm(forms.ModelForm):
    class Meta:
        model = models.Urls
        fields = [
            "path",
        ]