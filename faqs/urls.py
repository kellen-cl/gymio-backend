from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.FAQCategoryViewSet, basename='category')
router.register('', views.FAQViewSet, basename='faq')

urlpatterns = [
    path('', include(router.urls)),
]