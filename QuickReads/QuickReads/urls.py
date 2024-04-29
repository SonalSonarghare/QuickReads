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
from django.urls import path,include
from QuickReads import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index),  # Define the root URL pattern
    path('index/', views.Index),
    path('Home/', views.Home, name='Home'),
    path('Health/',views.Health,name='Health'),
    path('Technology/',views.Technology,name='Technology'),
    path('Education/',views.Education,name='Education'),
    path('Movies/',views.Movies),
    path('Politics/',views.Politics),
    path('Nature/',views.Nature),
    path('Travel/',views.Travel),
    path('Sports/',views.Sports,name='Sports'),
    path('Business/',views.Business,name='Business'),
    #path('Hybrid/',views.Hybrid),
    path('Login/',views.Login,name='Login'),
    path('Register/',views.Register,name='Register'),
    path('Logout/',views.logoutUser,name='Logout'),
    path('saved/',views.saved,name='saved'),
    path('add_bookmark/<str:pk>/', views.add_bookmark, name='add_bookmark'),
    path('remove_bookmark/<str:pk>/', views.remove_bookmark, name='remove_bookmark'),
    path('like/',views.like,name='like'),
    path('add_Like/<str:pk>/', views.add_Like, name='add_Like'),
    path('remove_Like/<str:pk>/', views.remove_Like, name='remove_Like'),
    path('csv/', views.csv_forall, name='csv'),
    path('my_view/', views.my_view, name='my_view')
]
