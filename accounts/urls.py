from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.get_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('change-password/', views.change_password, name='change-password'),
    path('', include(router.urls)),
]
