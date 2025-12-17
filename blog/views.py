from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import BlogPost, BlogCategory, BlogComment
from .serializers import BlogPostSerializer, BlogCategorySerializer, BlogCommentSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published')
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer


class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.filter(is_approved=True)
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
