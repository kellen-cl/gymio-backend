from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.BookingViewSet, basename='booking')
router.register('reviews', views.ClassReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
