from rest_framework import serializers
from .models import GymClass

class GymClassSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.full_name', read_only=True)
    enrolled_count = serializers.ReadOnlyField()
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    waitlist_count = serializers.ReadOnlyField()
    
    class Meta:
        model = GymClass
        fields = '__all__'