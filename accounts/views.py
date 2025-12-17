from rest_framework import status, generics, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Attendance
from .serializers import (
    UserRegistrationSerializer, UserSerializer, UserProfileUpdateSerializer,
    ChangePasswordSerializer, AttendanceSerializer, UserListSerializer
)

# Create your views here.

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return JWT tokens"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Please provide both email and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.check_password(password):
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return Response({
            'error': 'Account is deactivated'
        }, status=status.HTTP_403_FORBIDDEN)
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'message': 'Login successful',
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """Update current user profile"""
    serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'user': UserSerializer(request.user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """CRUD operations for users (Admin only)"""
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # Filtering
        role = self.request.query_params.get('role')
        membership_status = self.request.query_params.get('membership_status')
        search = self.request.query_params.get('search')
        
        if role:
            queryset = queryset.filter(role=role)
        if membership_status:
            queryset = queryset.filter(membership_status=membership_status)
        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        """Check in a member"""
        user = self.get_object()
        
        if user.membership_status != 'active':
            return Response({
                'error': 'Member does not have an active membership'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create attendance record
        attendance = Attendance.objects.create(member=user)
        
        # Update user check-in info
        user.last_check_in = timezone.now()
        user.total_check_ins += 1
        user.save()
        
        return Response({
            'message': f'{user.full_name} checked in successfully',
            'attendance': AttendanceSerializer(attendance).data
        })
    
    @action(detail=False, methods=['put'], url_path='check-out/(?P<attendance_id>[^/.]+)')
    def check_out(self, request, attendance_id=None):
        """Check out a member"""
        try:
            attendance = Attendance.objects.get(id=attendance_id)
        except Attendance.DoesNotExist:
            return Response({
                'error': 'Attendance record not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if attendance.check_out_time:
            return Response({
                'error': 'Member already checked out'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        attendance.check_out_time = timezone.now()
        attendance.save()
        
        return Response({
            'message': 'Checked out successfully',
            'attendance': AttendanceSerializer(attendance).data
        })
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user statistics"""
        user = self.get_object()
        
        attendances = Attendance.objects.filter(member=user)
        total_visits = attendances.count()
        
        # Calculate average duration
        durations = [a.duration_minutes for a in attendances if a.duration_minutes]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Recent attendances
        recent = attendances[:10]
        
        return Response({
            'total_visits': total_visits,
            'average_duration': round(avg_duration, 2),
            'recent_attendances': AttendanceSerializer(recent, many=True).data
        })