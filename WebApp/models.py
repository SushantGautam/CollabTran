from difflib import Differ

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Contribution(models.Model):
    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    Original = models.TextField(max_length=10000000, default="")
    Submission = models.TextField(max_length=10000000, default="")
    EditURL = models.TextField(max_length=100000, null=False, blank=False)
    EditxPath = models.TextField(max_length=100000, null=False, blank=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("WebApp_Contribution_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("WebApp_Contribution_update", args=(self.pk,))

    def getDifference(self):
        justOlderValue = ""
        contribution = Contribution.objects.filter(EditxPath=self.EditxPath, EditURL=self.EditURL,
                                                   created__lt=self.created).order_by('-created')
        if contribution.count():
            justOlderValue = contribution[0].Submission
        # return " ".join(list(Differ().compare(.split(), )))

        diff = " ".join(
            [i for i in list(Differ().compare(justOlderValue.split(), self.Submission.split())) if i != '? ^\n'])
        return diff


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
