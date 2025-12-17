from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import GymClass
from .serializers import GymClassSerializer

class GymClassViewSet(viewsets.ModelViewSet):
    queryset = GymClass.objects.filter(is_active=True)
    serializer_class = GymClassSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return []
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = GymClass.objects.filter(is_active=True)
        
        # Filtering
        category = self.request.query_params.get('category')
        difficulty = self.request.query_params.get('difficulty')
        day_of_week = self.request.query_params.get('day_of_week')
        
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if day_of_week:
            queryset = queryset.filter(day_of_week=int(day_of_week))
        
        return queryset