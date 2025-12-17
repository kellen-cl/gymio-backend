from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Sum, Count
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'stats']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_revenue = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        by_status = Payment.objects.values('status').annotate(
            count=Count('id'),
            total=Sum('amount')
        )
        
        return Response({
            'total_revenue': total_revenue,
            'by_status': list(by_status)
        })
