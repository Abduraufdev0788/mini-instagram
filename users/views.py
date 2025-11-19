from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse

class Register(View):
    def post(request:HttpRequest)->HttpResponse:
        return render(request=request, template_name="register.html")
