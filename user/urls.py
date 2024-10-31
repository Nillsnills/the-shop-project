from django.urls import path
from .views import register_view, logout_custom
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_custom, name='logout'),
]