from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    plan_name = serializers.CharField(source='membership_plan.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['invoice_number', 'created_at']
