from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import FAQ, FAQCategory
from .serializers import FAQSerializer, FAQCategorySerializer
from django.db.models import Q



class FAQViewSet(viewsets.ModelViewSet):
    """
    API endpoint for FAQs
    
    list/retrieve: Public
    create/update/destroy: Admin only
    """
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'helpful']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        
        # Non-admin only sees active FAQs
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(question__icontains=search) |
                Q(answer__icontains=search)
            )
        
        return queryset.order_by('category__order', 'order', 'question')
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get single FAQ and increment view count
        """
        instance = self.get_object()
        
        # Increment views
        instance.views += 1
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def helpful(self, request, pk=None):
        """
        Mark FAQ as helpful
        """
        faq = self.get_object()
        faq.helpful_count += 1
        faq.save()
        
        return Response({
            'message': 'Thank you for your feedback!',
            'helpful_count': faq.helpful_count
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def popular(self, request):
        """
        Get most viewed FAQs
        """
        limit = int(request.query_params.get('limit', 5))
        faqs = FAQ.objects.filter(
            is_active=True
        ).order_by('-views')[:limit]
        
        return Response(FAQSerializer(faqs, many=True).data)


class FAQCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for FAQ categories
    
    list/retrieve: Public
    create/update/destroy: Admin only
    """
    queryset = FAQCategory.objects.all()
    serializer_class = FAQCategorySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        return FAQCategory.objects.all().order_by('order', 'name')
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def with_faqs(self, request):
        """
        Get all categories with their FAQs
        """
        categories = FAQCategory.objects.prefetch_related('faqs').all()
        
        data = []
        for category in categories:
            faqs = category.faqs.filter(is_active=True)
            data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'faqs': FAQSerializer(faqs, many=True).data
            })
        
        return Response(data)