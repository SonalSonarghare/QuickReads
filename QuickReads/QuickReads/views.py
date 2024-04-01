from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def Index(request):
    return render(request, "index.html")

def Login(request):
     if request.user.is_authenticated:
        return redirect('Home')
     else:
        if request.method == "POST":
            username = request.POST.get('username') 
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("Home")
            else:
                error_message = 'Invalid username or password.'
                return render(request, "Login.html", {'error_message': error_message})
        else:
            return render(request, "Login.html")

def Register(request):
    if request.user.is_authenticated:
        return redirect('Home')
    else:
        form = CreateUserForm()
        if request.method=="POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username') 
                messages.success(request,'Account Created Successfully for'+ user)
                return redirect('Login')
        context = {'form':form}
        return render(request, "Register.html",context)


def logoutUser(request):
    logout(request)
    return redirect('Login')

@login_required(login_url='Login')
def Home(request):
    return render(request, "home.html")

@login_required(login_url='Login')
def Health(request):
    return render(request, "Health.html")



    
