from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Media
    icon = models.CharField(max_length=50, blank=True, help_text='Icon class name')
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    
    # Details
    features = models.JSONField(default=list, help_text='List of service features')
    
    # Status
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text='Display order')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name