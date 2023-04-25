from rest_framework import serializers
# from .models import ClassificationModel


class ClassificationSerializer(serializers.Serializer):
    prediction = serializers.IntegerField()
    confidence = serializers.FloatField()
