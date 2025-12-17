from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class GymClass(models.Model):
    CATEGORY_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('hiit', 'HIIT'),
        ('dance', 'Dance'),
        ('martial-arts', 'Martial Arts'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    DAY_CHOICES = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='beginner')
    
    # Instructor
    instructor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='classes_taught', limit_choices_to={'role': 'trainer'})
    
    # Schedule
    day_of_week = models.IntegerField(choices=DAY_CHOICES, validators=[MinValueValidator(0), MaxValueValidator(6)])
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.IntegerField(default=60)
    
    # Capacity
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Location
    room = models.CharField(max_length=100, blank=True)
    
    # Equipment
    equipment_needed = models.TextField(blank=True, help_text='List equipment needed')
    
    # Media
    image = models.ImageField(upload_to='class_images/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text='YouTube or Vimeo URL')
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = 'Gym Class'
        verbose_name_plural = 'Gym Classes'
    
    def __str__(self):
        return f"{self.name} - {self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')}"
    
    @property
    def enrolled_count(self):
        return self.bookings.filter(status='confirmed').count()
    
    @property
    def available_spots(self):
        return max(0, self.capacity - self.enrolled_count)
    
    @property
    def is_full(self):
        return self.enrolled_count >= self.capacity
    
    @property
    def waitlist_count(self):
        return self.bookings.filter(status='waitlist').count()