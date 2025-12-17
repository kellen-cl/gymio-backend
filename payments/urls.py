from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('stats/', views.PaymentViewSet.as_view({'get': 'stats'}), name='payment-stats'),
    path('', include(router.urls)),
]