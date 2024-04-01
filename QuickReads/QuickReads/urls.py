"""
URL configuration for QuickReads project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from QuickReads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index),  # Define the root URL pattern
    path('index/', views.Index),
    path('Home/', views.Home, name='Home'),
    path('Health/',views.Health),
    path('Login/',views.Login,name='Login'),
    path('Register/',views.Register,name='Register'),
    path('Logout/',views.logoutUser,name='Logout'),

]