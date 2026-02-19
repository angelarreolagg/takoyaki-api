from rest_framework import serializers
from .models import RawBlogsEntries


class RawBlogsEntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawBlogsEntries
        fields = [
            "main_image_url",
            "title",
            "subtitle",
            "info_subtitles",
            "info_data",
        ]
