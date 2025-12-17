from django.db import models
from django.utils import timezone

# Create your models here.
class MembershipPlan(models.Model):
    DURATION_TYPE_CHOICES = [
        ('days', 'Days'),
        ('months', 'Months'),
        ('years', 'Years'),
    ]
    
    ACCESS_HOURS_CHOICES = [
        ('24/7', '24/7 Access'),
        ('peak', 'Peak Hours Only'),
        ('off-peak', 'Off-Peak Hours'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Duration
    duration = models.IntegerField(help_text='Duration value')
    duration_type = models.CharField(max_length=10, choices=DURATION_TYPE_CHOICES, default='months')
    
    # Features
    features = models.JSONField(default=list, help_text='List of plan features')
    classes_per_week = models.IntegerField(null=True, blank=True, help_text='Null means unlimited')
    personal_training_sessions = models.IntegerField(default=0)
    access_hours = models.CharField(max_length=20, choices=ACCESS_HOURS_CHOICES, default='24/7')
    
    # Styling
    color = models.CharField(max_length=7, default='#3B82F6', help_text='Hex color code')
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class or name')
    
    # Payment Integration
    stripe_price_id = models.CharField(max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['price']
        verbose_name = 'Membership Plan'
        verbose_name_plural = 'Membership Plans'
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    @property
    def duration_display(self):
        return f"{self.duration} {self.duration_type}"


class MembershipSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    
    # Dates
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    
    # Auto Renewal
    auto_renew = models.BooleanField(default=False)
    
    # Payment Info
    payment = models.ForeignKey('payments.Payment', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
    
    def __str__(self):
        return f"{self.user.full_name} - {self.plan.name}"
    
    @property
    def is_active(self):
        return self.status == 'active' and self.end_date >= timezone.now().date()
    
    @property
    def days_remaining(self):
        if self.end_date:
            delta = self.end_date - timezone.now().date()
            return max(0, delta.days)
        return 0