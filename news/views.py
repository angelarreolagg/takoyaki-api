from rest_framework import viewsets
from core.models import BlogProcessedEntries
from core.serializers import BlogProcessedEntriesSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = BlogProcessedEntries.objects.all()
    serializer_class = BlogProcessedEntriesSerializer