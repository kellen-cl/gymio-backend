from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Booking, ClassReview
from .serializers import BookingSerializer, ClassReviewSerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    def create(self, request):
        gym_class_id = request.data.get('gym_class')
        class_date = request.data.get('class_date')
        
        from classes.models import GymClass
        try:
            gym_class = GymClass.objects.get(id=gym_class_id)
        except GymClass.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if class is full
        confirmed_bookings = Booking.objects.filter(
            gym_class=gym_class,
            class_date=class_date,
            status='confirmed'
        ).count()
        
        booking_status = 'confirmed' if confirmed_bookings < gym_class.capacity else 'waitlist'
        
        booking = Booking.objects.create(
            user=request.user,
            gym_class=gym_class,
            class_date=class_date,
            status=booking_status
        )
        
        message = 'Booking confirmed' if booking_status == 'confirmed' else 'Added to waitlist'
        
        return Response({
            'message': message,
            'booking': BookingSerializer(booking).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        
        if booking.user != request.user and request.user.role != 'admin':
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        reason = request.data.get('reason', '')
        booking.cancel(reason)
        
        return Response({'message': 'Booking cancelled successfully'})


class ClassReviewViewSet(viewsets.ModelViewSet):
    queryset = ClassReview.objects.all()
    serializer_class = ClassReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

