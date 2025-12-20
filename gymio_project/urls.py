from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from .views import api_home  # Import the new view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Beautiful API landing page
    path('', api_home, name='api-home'),  # Root URL
    path('api/', api_home, name='api-root'),  # Also on /api/
    
    # API endpoints
    path('api/auth/', include('accounts.urls')),
    path('api/memberships/', include('memberships.urls')),
    path('api/classes/', include('classes.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/services/', include('services.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/faqs/', include('faqs.urls')),
    
    # JWT token refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)