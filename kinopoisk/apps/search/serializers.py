from rest_framework import serializers


class SearchResultSerializer(serializers.Serializer):
    type = serializers.CharField()                 # 'movie' | 'person' | 'news'
    id = serializers.IntegerField()
    title = serializers.CharField()
    url = serializers.CharField()
    poster = serializers.ImageField(required=False, allow_null=True)
    year = serializers.IntegerField()

    # TODO: при желании добавьте 'year' или 'description'
