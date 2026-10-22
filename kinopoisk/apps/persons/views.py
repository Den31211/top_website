from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Person
from .serializers import PersonSerializer, PersonListSerializer


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return PersonListSerializer
        return PersonSerializer
