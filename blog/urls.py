from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.BlogPostViewSet, basename='post')
router.register('categories', views.BlogCategoryViewSet, basename='category')
router.register('comments', views.BlogCommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]