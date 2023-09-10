from django.urls import path

from accounts.views import (
    SignupView,
    ProfileView,
    LogOutView,
    LoginView,
)

urlpatterns = [
    path("registration/", SignupView.as_view(), name="registration"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("signout/", LogOutView.as_view(), name="logout"),
]
