from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv

import random
import os

from .models import Users

load_dotenv()


# ========================= REGISTER =========================
class Register(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "register.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        image = request.FILES.get("image")

        # ===== Validations =====
        if not first_name:
            return JsonResponse({"first_name": "required"}, status=403)
        if len(first_name) > 128:
            return JsonResponse({"first_name": "max 128 characters"}, status=403)
        
        if not last_name:
            return JsonResponse({"last_name": "required"}, status=403)
        if len(last_name) > 128:
            return JsonResponse({"last_name": "max 128 characters"}, status=403)
        
        if not username:
            return JsonResponse({"username": "required"}, status=403)
        if len(username) > 128:
            return JsonResponse({"username": "max 128 characters"}, status=403)
        if not username.startswith("@"):
            return JsonResponse({"username": "must start with @"}, status=403)
        if Users.objects.filter(username=username).exists():
            return JsonResponse({"username": "This username is busy"}, status=403)
        
        if not email:
            return JsonResponse({"email": "required"}, status=403)
        if not email.endswith("@gmail.com"):
            return JsonResponse({"email": "must be @gmail.com"}, status=403)
        if Users.objects.filter(email=email).exists():
            return JsonResponse({"email": "This email is busy"}, status=403)
        
        if not password:
            return JsonResponse({"password": "required"}, status=403)
        if len(password) < 8:
            return JsonResponse({"password": "min 8 characters"}, status=403)
        if len(password) > 256:
            return JsonResponse({"password": "max 256 characters"}, status=403)
        if not password.isalnum():
            return JsonResponse({"password": "must consist of letters and numbers"}, status=403)
        if password != confirm_password:
            return JsonResponse({"password": "passwords do not match"}, status=403)
        
        # ===== Save User =====
        new_user = Users(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=make_password(password),
            image=image
        )
        new_user.save()

        return render(request=request, template_name="home.html")


# ========================= LOGIN =========================
class Login(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "login.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username:
            return JsonResponse({"username": "required"}, status=403)
        if not password:
            return JsonResponse({"password": "required"}, status=403)

        user = Users.objects.filter(username=username).first()
        if not user:
            return JsonResponse({"message": "user not found"}, status=404)
        if not check_password(password, user.password):
            return JsonResponse({"message": "incorrect password"}, status=403)

        request.session["user_id"] = user.id
        return render(request=request, template_name="home.html")


# ========================= SEND RESET CODE =========================
def send_reset_code(email):
    code = random.randint(100000, 999999)
    send_mail(
        subject="Parolni tiklash kodi",
        message=f"Sizning tasdiqlash kodingiz: {code}",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[email],
    )
    return str(code)  # string sifatida saqlash


# ========================= FORGOT PASSWORD =========================
class ForgotPass(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "forgot.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"message": "email required"}, status=403)
        user = Users.objects.filter(email=email).first()
        if not user:
            return JsonResponse({"message": "user not found"}, status=404)
        
        code = send_reset_code(email)
        request.session["reset_code"] = code
        request.session["reset_email"] = email

        return render(request, "v_code.html", {"user": user})


# ========================= CODE VALIDATE =========================
class CodeValidate(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        email = request.session.get("reset_email")
        if not email:
            return JsonResponse({"message": "email not found"}, status=403)
        user = Users.objects.get(email=email)
        return render(request, "v_code.html", {"user": user})
    
    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.session.get("reset_email")
        saved_code = request.session.get("reset_code")
        code = request.POST.get("code")
        user = Users.objects.get(email=email)

        if not code:
            return JsonResponse({"message": "code required"}, status=401)
        if code != saved_code:
            return JsonResponse({"message": "invalid code"}, status=403)
        
        return render(request=request, template_name="reset_pass.html", context={"user":user})


# ========================= RESET PASSWORD =========================
class ResetPass(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        email = request.session.get("reset_email")
        if not email:
            return JsonResponse({"message": "email not found"}, status=403)
        
        return render(request, "reset_pass.html")
    
    def post(self, request: HttpRequest) -> HttpResponse:
        email = request.session.get("reset_email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not password:
            return JsonResponse({"message": "password required"}, status=403)
        if len(password) < 8:
            return JsonResponse({"message": "min 8 characters"}, status=403)
        if len(password) > 256:
            return JsonResponse({"message": "max 256 characters"}, status=403)
        if not password.isalnum():
            return JsonResponse({"message": "must consist of letters and numbers"}, status=403)
        if password != confirm_password:
            return JsonResponse({"message": "passwords do not match"}, status=403)

        user = Users.objects.get(email=email)
        user.password = make_password(password)
        user.save()

        return render(request=request, template_name="home.html")
    

class Profile(View):
    def get(self, request:HttpRequest)->HttpResponse:
        return render(request=request, template_name="home.html")
