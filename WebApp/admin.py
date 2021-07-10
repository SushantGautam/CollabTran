from django import forms
from django.contrib import admin

from . import models


class ContributionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Contribution
        fields = "__all__"


class ContributionAdmin(admin.ModelAdmin):
    form = ContributionAdminForm
    list_display = [
        "last_updated",
        "created",
        "User","EditxPath", "EditURL"
    ]
    readonly_fields = [
        "last_updated",
        "created",
        # "User",
    ]


class VotesAdminForm(forms.ModelForm):
    class Meta:
        model = models.Votes
        fields = "__all__"


class VotesAdmin(admin.ModelAdmin):
    form = VotesAdminForm
    list_display = [
        "last_updated",
        "created",
        "contribution",
        "voter",
        "type",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


admin.site.register(models.Contribution, ContributionAdmin)
admin.site.register(models.Votes, VotesAdmin)
