from rest_framework import serializers
from .models import FAQ, FAQCategory

class FAQSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = FAQ
        fields = '__all__'


class FAQCategorySerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True, read_only=True)
    
    class Meta:
        model = FAQCategory
        fields = '__all__'