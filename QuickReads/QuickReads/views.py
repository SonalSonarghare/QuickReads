from django.http import HttpResponse
from django.shortcuts import render, redirect

def Index(request):
    return render(request, "index.html")

def Home(request):
    return render(request, "home.html")

def Health(request):
    return render(request, "Health.html")

def Login(request):
    return render(request, "Login.html")

def Register(request):
    return render(request, "Register.html")
