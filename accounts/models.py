from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
    # Set these BEFORE creating the user
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('first_name', extra_fields.get('first_name', 'Admin'))
        extra_fields.setdefault('last_name', extra_fields.get('last_name', 'User'))
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    MEMBERSHIP_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    ]
    
    # Basic Info
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    # Address
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Kenya')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Profile
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bio = models.TextField(blank=True)
    
    # Role & Status
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    membership_status = models.CharField(max_length=15, choices=MEMBERSHIP_STATUS_CHOICES, default='inactive')
    
    # Membership Details
    membership_plan = models.ForeignKey('memberships.MembershipPlan', on_delete=models.SET_NULL, null=True, blank=True)
    membership_start_date = models.DateField(null=True, blank=True)
    membership_end_date = models.DateField(null=True, blank=True)
    
    # Medical Info
    medical_conditions = models.TextField(blank=True, help_text='List any medical conditions')
    medications = models.TextField(blank=True, help_text='Current medications')
    allergies = models.TextField(blank=True, help_text='Known allergies')
    injuries = models.TextField(blank=True, help_text='Past or current injuries')
    
    # Fitness Goals
    fitness_goals = models.TextField(blank=True, help_text='Member fitness goals')
    
    # Activity Tracking
    last_check_in = models.DateTimeField(null=True, blank=True)
    total_check_ins = models.IntegerField(default=0)
    
    # Account Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_membership_active(self):
        if not self.membership_end_date:
            return False
        return self.membership_end_date >= timezone.now().date()


class Attendance(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    gym_class = models.ForeignKey('classes.GymClass', on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-check_in_time']
        verbose_name_plural = 'Attendances'
    
    def __str__(self):
        return f"{self.member.full_name} - {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        # Calculate duration if check_out_time is set
        if self.check_out_time and self.check_in_time:
            delta = self.check_out_time - self.check_in_time
            self.duration_minutes = int(delta.total_seconds() / 60)
        super().save(*args, **kwargs)