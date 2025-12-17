from django.db import models
from django.utils.text import slugify
from django.db.models import Q

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text='Short description for preview')
    content = models.TextField()
    
    # Relations
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.CharField(max_length=200, blank=True, help_text='Comma-separated tags')
    
    # Media
    featured_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    
    # Engagement
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    # Dates
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def reading_time(self):
        # Estimate reading time (average 200 words per minute)
        word_count = len(self.content.split())
        minutes = word_count / 200
        return max(1, round(minutes))


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='blog_comments')
    
    content = models.TextField()
    
    # Moderation
    is_approved = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Comment'
        verbose_name_plural = 'Blog Comments'
    
    def __str__(self):
        return f"{self.user.full_name} on {self.post.title}"