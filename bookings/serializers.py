from rest_framework import serializers
from .models import Booking, ClassReview
from classes.serializers import GymClassSerializer  # ✅ import from OTHER app

class BookingSerializer(serializers.ModelSerializer):
    class_details = GymClassSerializer(source='gym_class', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_date', 'check_in_time']


class ClassReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = ClassReview
        fields = '__all__'
