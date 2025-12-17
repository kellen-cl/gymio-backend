from django.db import models
from django.utils import timezone

# Create your models here.
class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('membership', 'Membership Question'),
        ('classes', 'Classes Information'),
        ('personal_training', 'Personal Training'),
        ('facilities', 'Facilities Question'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    # Contact Info
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Message
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    
    # User (if logged in)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_messages')
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    
    # Admin Response
    admin_notes = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    replied_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_replies')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"


class GymInfo(models.Model):
    # Contact Details
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Operating Hours
    operating_hours = models.JSONField(default=dict, help_text='Operating hours by day')
    
    # Map
    map_embed_url = models.TextField(blank=True, help_text='Google Maps embed URL')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Metadata
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Gym Information'
        verbose_name_plural = 'Gym Information'
    
    def __str__(self):
        return f"Gym Contact Information"
