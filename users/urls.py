from django.urls import path
from .views import Register, Login, ForgotPass

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("forgot/", ForgotPass.as_view(), name="forgot_email")
]
