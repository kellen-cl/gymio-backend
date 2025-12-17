from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Attendance

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'password_confirm', 
                  'date_of_birth', 'gender']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    is_membership_active = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 
                  'date_of_birth', 'gender', 'profile_image', 'bio', 'role', 
                  'membership_status', 'membership_plan', 'membership_start_date', 
                  'membership_end_date', 'is_membership_active', 'street_address', 'city', 
                  'state', 'zip_code', 'country', 'fitness_goals', 'last_check_in', 
                  'total_check_ins', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'last_check_in', 'total_check_ins']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth', 'gender', 
                  'profile_image', 'bio', 'street_address', 'city', 'state', 'zip_code', 
                  'country', 'emergency_contact_name', 'emergency_contact_phone', 
                  'emergency_contact_relationship', 'medical_conditions', 'medications', 
                  'allergies', 'injuries', 'fitness_goals']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match")
        return data


class AttendanceSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.full_name', read_only=True)
    class_name = serializers.CharField(source='gym_class.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['check_in_time', 'duration_minutes']


class UserListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing users"""
    full_name = serializers.ReadOnlyField()
    membership_plan_name = serializers.CharField(source='membership_plan.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 
                  'role', 'membership_status', 'membership_plan_name', 'profile_image', 
                  'date_joined']