from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from .models import Users

class Register(View):
    def get(self, request:HttpRequest)->HttpResponse:
        return render(request=request, template_name="register.html")
    

    def post(self,request:HttpRequest)->HttpResponse:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        image = request.FILES.get("image")


        if not first_name:
            return JsonResponse({"first_name": "required"}, status =403)
        if len(first_name) >128:
            return JsonResponse({'message': 'max 128 characters'})
        

        if not last_name:
            return JsonResponse({"last_name": "required"}, status =403)
        if len(last_name) >128:
            return JsonResponse({'message': 'max 128 characters'})
        
        if not username:
            return JsonResponse({"username":"required"}, status = 403)
        if len("username")> 128:
            return JsonResponse({"message": "max 128 characters"}, status = 403)
        if Users.objects.filter(username=username).exists():
            return JsonResponse({"message": "This username is busy"}, status = 403)
        if not username.startswith("@"):
            return JsonResponse({"message": "Must start with @"}, status = 403)
        
        if not email:
            return JsonResponse({"message": "email required"}, status = 403)
        if Users.objects.filter(email=email).exists():
            return JsonResponse({"message": "This username is busy"}, status = 403)
        if not email.endswith("@gmail.com"):
            return JsonResponse({"message": "It should be @gmail.com after all."}, status = 403)
        
        if not password:
            return JsonResponse({"message": "password required"})
        if len(password) < 8:
            return JsonResponse({"message": "min 8 characters"})
        if len(password) > 256:
            return JsonResponse({"message": "max 256 characters"})
        if not password.isalnum():
            return JsonResponse({"message": "must consist of letters and numbers"}, status = 403)
        
        new_user = Users(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            password = password,
            image = image
        )

        new_user.save()
        return JsonResponse({"message": "succes"})
    

class Login(View):
    def get(self,request: HttpRequest)->HttpResponse:
        return render(request=request, template_name="login.html")
    
    def post(self, request:HttpRequest)->HttpResponse:
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username:
            return JsonResponse({"message":"username required"}, status = 403)
        
        if not password:
            return JsonResponse({"message": "password required"})
        
        user =Users.objects.get(username = username)

        if user.password != password:
            return JsonResponse({"message": "incorrect password"}, status=403)
        
        request.session["user_id"] = user.id

        return JsonResponse({"message": "login success"})
