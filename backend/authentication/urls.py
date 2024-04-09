from django.urls import path
from .views import (signup, login, logout, join_family, create_family)

urlpatterns = [
    path("signup/", signup),
    path("login/", login),
    path("logout/", logout),
    path('join-family/', join_family),
    path('create-family/', create_family),
]
