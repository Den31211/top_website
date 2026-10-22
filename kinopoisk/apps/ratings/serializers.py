from rest_framework import serializers
from .models import Rating, Review


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'score', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate_score(self, value):
        #  TODO: проверьте, что оценка в диапазоне 1–10
        #  подсказка: if not 1 <= value <= 10: raise serializers.ValidationError(...)
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Введите корректную оценку: от 1 до 10')


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'text', 'is_spoiler', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
