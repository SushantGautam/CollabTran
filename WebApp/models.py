from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Contribution(models.Model):
    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("WebApp_Contribution_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("WebApp_Contribution_update", args=(self.pk,))


class Urls(models.Model):
    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    path = models.URLField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("WebApp_Urls_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("WebApp_Urls_update", args=(self.pk,))
