from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils import timezone
from datetime import timedelta
from .models import MembershipPlan, MembershipSubscription
from .serializers import MembershipPlanSerializer, MembershipSubscriptionSerializer


class MembershipPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for membership plans
    
    list: Get all active membership plans (Public)
    retrieve: Get single plan details (Public)
    create: Create new plan (Admin only)
    update: Update plan (Admin only)
    destroy: Delete plan (Admin only)
    """
    queryset = MembershipPlan.objects.filter(is_active=True)
    serializer_class = MembershipPlanSerializer
    
    def get_permissions(self):
        # List and retrieve are public
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        # Everything else requires admin
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = MembershipPlan.objects.all()
        
        # Filter only active plans for non-admin users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by featured
        is_featured = self.request.query_params.get('featured')
        if is_featured:
            queryset = queryset.filter(is_featured=True)
        
        return queryset.order_by('price')
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        """
        Subscribe current user to this plan
        """
        plan = self.get_object()
        user = request.user
        
        # Check if user already has an active subscription
        active_sub = MembershipSubscription.objects.filter(
            user=user,
            status='active',
            end_date__gte=timezone.now().date()
        ).first()
        
        if active_sub:
            return Response({
                'error': 'You already have an active subscription',
                'current_subscription': MembershipSubscriptionSerializer(active_sub).data
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate end date
        start_date = timezone.now().date()
        if plan.duration_type == 'days':
            end_date = start_date + timedelta(days=plan.duration)
        elif plan.duration_type == 'months':
            end_date = start_date + timedelta(days=plan.duration * 30)
        elif plan.duration_type == 'years':
            end_date = start_date + timedelta(days=plan.duration * 365)
        
        # Create subscription
        subscription = MembershipSubscription.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status='pending'  # Will be activated after payment
        )
        
        # Update user membership info
        user.membership_plan = plan
        user.membership_start_date = start_date
        user.membership_end_date = end_date
        user.membership_status = 'pending'
        user.save()
        
        return Response({
            'message': 'Subscription created. Please complete payment.',
            'subscription': MembershipSubscriptionSerializer(subscription).data
        }, status=status.HTTP_201_CREATED)


class MembershipSubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for membership subscriptions
    
    Admin can see all subscriptions
    Users can only see their own subscriptions
    """
    serializer_class = MembershipSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin sees all subscriptions
        if user.role == 'admin':
            queryset = MembershipSubscription.objects.all()
            
            # Filter by user if specified
            user_id = self.request.query_params.get('user')
            if user_id:
                queryset = queryset.filter(user_id=user_id)
            
            # Filter by status
            status_filter = self.request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            return queryset
        
        # Regular users only see their own subscriptions
        return MembershipSubscription.objects.filter(user=user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        """
        Activate a subscription (Admin only)
        Usually called after payment confirmation
        """
        subscription = self.get_object()
        
        subscription.status = 'active'
        subscription.save()
        
        # Update user status
        user = subscription.user
        user.membership_status = 'active'
        user.save()
        
        return Response({
            'message': 'Subscription activated successfully',
            'subscription': MembershipSubscriptionSerializer(subscription).data
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a subscription
        """
        subscription = self.get_object()
        
        # Check permission (user can cancel own, admin can cancel any)
        if subscription.user != request.user and request.user.role != 'admin':
            return Response({
                'error': 'Not authorized to cancel this subscription'
            }, status=status.HTTP_403_FORBIDDEN)
        
        subscription.status = 'cancelled'
        subscription.save()
        
        # Update user status
        user = subscription.user
        user.membership_status = 'inactive'
        user.save()
        
        return Response({
            'message': 'Subscription cancelled successfully'
        })