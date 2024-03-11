from django.http import HttpResponse
from django.shortcuts import render

def Index(request):
    return render(request,"index.html")


def Home(request):
    return render(request,"home.html")

def Health(request):
    return render(request, "Health.html")

