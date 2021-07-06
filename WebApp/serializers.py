from rest_framework import serializers

from . import models


class ContributionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Contribution
        fields = [
            "last_updated",
            "created",
            "User",
        ]

class UrlsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Urls
        fields = [
            "last_updated",
            "created",
            "path",
        ]