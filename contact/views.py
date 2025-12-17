from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.utils import timezone
from .models import ContactMessage, GymInfo
from .serializers import ContactMessageSerializer, GymInfoSerializer


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for contact messages
    
    create: Public (anyone can submit)
    list/retrieve/update/destroy: Admin only
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by subject
        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(subject=subject)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        Create contact message
        Auto-link to user if authenticated
        """
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Submit contact form
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # You can add email notification here
        # send_email_to_admin(serializer.data)
        
        return Response({
            'message': 'Thank you for contacting us! We will get back to you soon.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_read(self, request, pk=None):
        """
        Mark message as read
        """
        message = self.get_object()
        message.status = 'read'
        message.save()
        
        return Response({
            'message': 'Message marked as read',
            'data': ContactMessageSerializer(message).data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reply(self, request, pk=None):
        """
        Reply to message
        """
        message = self.get_object()
        
        admin_notes = request.data.get('admin_notes', '')
        
        message.status = 'replied'
        message.admin_notes = admin_notes
        message.replied_at = timezone.now()
        message.replied_by = request.user
        message.save()
        
        # You can add email notification here
        # send_reply_email(message)
        
        return Response({
            'message': 'Reply sent successfully',
            'data': ContactMessageSerializer(message).data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def unread(self, request):
        """
        Get unread messages count
        """
        count = ContactMessage.objects.filter(status='new').count()
        
        return Response({
            'unread_count': count
        })


class GymInfoView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for gym information
    
    GET: Public (anyone can view)
    PUT/PATCH: Admin only
    """
    queryset = GymInfo.objects.all()
    serializer_class = GymInfoSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_object(self):
        """
        Get the first (and only) gym info object
        Create if doesn't exist
        """
        obj, created = GymInfo.objects.get_or_create(
            id=1,
            defaults={
                'phone': '+254712345678',
                'email': 'info@gymio.com',
                'address': '123 Fitness Street, Nairobi, Kenya'
            }
        )
        return obj
