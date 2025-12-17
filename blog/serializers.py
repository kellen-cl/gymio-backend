from rest_framework import serializers
from .models import BlogPost, BlogCategory, BlogComment

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    reading_time = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = BlogComment
        fields = '__all__'
