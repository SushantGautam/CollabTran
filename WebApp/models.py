from difflib import HtmlDiff

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
        ordering = ['-id']

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Contribution_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Contribution_update", args=(self.pk,))

    def TotalEditsOnThisPage(self):
        return Contribution.objects.filter(EditURL=self.EditURL)

    def getDifference(self):
        justOlderValue = ""
        contribution = Contribution.objects.filter(EditxPath=self.EditxPath, EditURL=self.EditURL,
                                                   created__lt=self.created).order_by('-created')
        if contribution.count():
            justOlderValue = contribution[0].Submission
        # return " ".join(list(Differ().compare(.split(), )))

        return HtmlDiff(wrapcolumn=40).make_file([justOlderValue], [self.Submission])


class Votes(models.Model):
    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=(('U', 'UpVote'), ('D', 'UpVote'),))

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Votes_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Votes_update", args=(self.pk,))
