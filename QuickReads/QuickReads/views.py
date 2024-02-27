from django.http import HttpResponse
from django.shortcuts import render

def Index(request):
    return render(request,"index.html")


def Login(request):
    return HttpResponse("Welcome to QuickReads")

def Register(request):
    return HttpResponse("Register")

def Home(request):
    return HttpResponse("Home")

def Home_articles(request,article1):
    return HttpResponse(article1)




    