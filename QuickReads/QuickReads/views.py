from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm,LoginForm
#authenticate model and Functions
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
def Index(request):
    return render(request, "index.html")

def Home(request):
    return render(request, "home.html")

def Health(request):
    return render(request, "Health.html")

def Login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("Home")
    context = {'loginform': form}
    return render(request, "Login.html", context)

def Register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()  # Saving the form after validation
            return redirect("Login")  # Redirecting to the login page after successful registration
    context = {'registerform': form}
    return render(request, "Register.html", context)
