from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('messages', views.ContactMessageViewSet, basename='message')

urlpatterns = [
    path('info/', views.GymInfoView.as_view(), name='gym-info'),
    path('', include(router.urls)),
]