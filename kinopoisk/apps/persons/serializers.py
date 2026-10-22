from rest_framework import serializers
from .models import Person, Role

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        #  TODO: перечислите поля (id, name, slug, photo, birth_date, biography)
        fields = ['id', 'name', 'slug', 'photo', 'birth_date', 'biography']


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'slug', 'photo']


class RoleSerializer(serializers.ModelSerializer):
    person = PersonListSerializer(read_only=True)

    class Meta:
        model = Role
        #  TODO: укажите поля (id, person, role_type, character_name)
        fields = ['id', 'person', 'role_type', 'character_name']
