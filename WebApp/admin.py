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


class UrlsAdminForm(forms.ModelForm):
    class Meta:
        model = models.Urls
        fields = "__all__"


class UrlsAdmin(admin.ModelAdmin):
    form = UrlsAdminForm
    list_display = [
        "last_updated",
        "created",
        "path",
    ]
    readonly_fields = [
        "last_updated",
        "created",
        # "path",
    ]


admin.site.register(models.Contribution, ContributionAdmin)
admin.site.register(models.Urls, UrlsAdmin)
