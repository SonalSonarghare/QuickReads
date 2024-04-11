from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import csv
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

#HEALTH
@login_required(login_url='Login')
def Health(request):
    articles = []
    # Specify the full path to the CSV file
    csv_file_path = r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\healthline_articles.csv'
    
    # Read data from CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {key.strip('\ufeff'): value for key, value in row.items()}
            articles.append(row)
    
    # Print articles for debugging
    print(articles)

    return render(request, "Health.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#TECHNOLOGY
@login_required(login_url='Login')
def Technology(request):
    articles = []
    # Specify the full path to the CSV file
    csv_file_path = r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Technology_articles.csv'
    
    # Read data from CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {key.strip('\ufeff'): value for key, value in row.items()}
            articles.append(row)
    
    # Print articles for debugging
    print(articles)

    return render(request, "Technology.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#EDUCATION
@login_required(login_url='Login')
def Education(request):
    articles = []
    # Specify the full path to the CSV file
    csv_file_path = r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Education_articles.csv'
    
    # Read data from CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {key.strip('\ufeff'): value for key, value in row.items()}
            articles.append(row)
    
    # Print articles for debugging
    print(articles)

    return render(request, "Education.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#MOVIES
@login_required(login_url='Login')
def Movies(request):
    articles = []
    # Specify the full path to the CSV file
    csv_file_path = r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Movies_articles.csv'
    
    # Read data from CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {key.strip('\ufeff'): value for key, value in row.items()}
            articles.append(row)
    
    # Print articles for debugging
    print(articles)

    return render(request, "Movies.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

       
    


       
    
