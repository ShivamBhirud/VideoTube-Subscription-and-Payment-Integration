from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView
from accounts.views import (
    SignUpView, LoginView, LogoutView)


urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
]