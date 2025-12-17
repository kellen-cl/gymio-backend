from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('plans', views.MembershipPlanViewSet, basename='plan')
router.register('subscriptions', views.MembershipSubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]