from rest_framework import serializers
from .models import MembershipPlan, MembershipSubscription

class MembershipPlanSerializer(serializers.ModelSerializer):
    duration_display = serializers.ReadOnlyField()
    
    class Meta:
        model = MembershipPlan
        fields = '__all__'


class MembershipSubscriptionSerializer(serializers.ModelSerializer):
    plan_details = MembershipPlanSerializer(source='plan', read_only=True)
    is_active = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = MembershipSubscription
        fields = '__all__'