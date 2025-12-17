from rest_framework import serializers
from .models import ContactMessage, GymInfo

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ['status', 'created_at']


class GymInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymInfo
        fields = '__all__'