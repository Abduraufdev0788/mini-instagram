from django.urls import path
from .views import Register, Login, ForgotPass, CodeValidate

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("forgot/", ForgotPass.as_view(), name="forgot_email"),
    path("verify-code/", CodeValidate.as_view(), name="verify_code"),
]
