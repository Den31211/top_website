from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsDetailSerializer
