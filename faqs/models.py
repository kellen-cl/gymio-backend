from django.db import models

# Create your models here.
class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'
    
    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    
    # Status
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    # Engagement
    views = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question