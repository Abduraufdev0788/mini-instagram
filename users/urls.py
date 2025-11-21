from django.urls import path
from .views import Register, Login, ForgotPass, CodeValidate, Profile, ResetPass

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("forgot/", ForgotPass.as_view(), name="forgot_email"),
    path("verify_code/", CodeValidate.as_view(), name="verify_code"),
    path("password_update/", ResetPass.as_view(), name="reset_pass"),
    path("home/", Profile.as_view(), name="home_page")
]
