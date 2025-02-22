from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.CustomTokenCreateView.as_view(), name="login"),
    path("verify-otp/", views.OTPVerifyView.as_view(), name="verify_otp"),
    path("refresh/", views.CustomTokenRefreshView.as_view(), name="refresh"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
]
