from django.db import models
from django.utils import timezone

# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('waitlist', 'Waitlist'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no-show', 'No Show'),
    ]
    
    # Relations
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookings')
    gym_class = models.ForeignKey('classes.GymClass', on_delete=models.CASCADE, related_name='bookings')
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='confirmed')
    
    # Dates
    booking_date = models.DateTimeField(auto_now_add=True)
    class_date = models.DateField(help_text='Specific date of the class')
    
    # Check-in
    checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-booking_date']
        unique_together = ['user', 'gym_class', 'class_date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
    
    def __str__(self):
        return f"{self.user.full_name} - {self.gym_class.name} on {self.class_date}"
    
    def cancel(self, reason=''):
        self.status = 'cancelled'
        self.cancellation_reason = reason
        self.save()
        
        # Move first person from waitlist to confirmed
        waitlist_booking = Booking.objects.filter(
            gym_class=self.gym_class,
            class_date=self.class_date,
            status='waitlist'
        ).order_by('booking_date').first()
        
        if waitlist_booking:
            waitlist_booking.status = 'confirmed'
            waitlist_booking.save()
    
    def check_in_member(self):
        self.checked_in = True
        self.check_in_time = timezone.now()
        self.save()


class ClassReview(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='class_reviews')
    gym_class = models.ForeignKey('classes.GymClass', on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    
    # Rating
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], help_text='1-5 stars')
    
    # Review
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'gym_class', 'booking']
        verbose_name = 'Class Review'
        verbose_name_plural = 'Class Reviews'
    
    def __str__(self):
        return f"{self.user.full_name} - {self.gym_class.name} ({self.rating}★)"