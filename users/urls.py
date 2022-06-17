
from django.contrib import admin
from django.urls import path
from users.views import (
    UserRegistrationView,
    HomePageView,
    UserListView,
    UserLoginView,
    UserLogoutView
)

app_name = "users"

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('users/all/', UserListView.as_view(), name="user_list"),
]
