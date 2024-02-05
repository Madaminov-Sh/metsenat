from django.urls import path, include
from users import views

# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('register/', views.SignUpAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
]