# models.py
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    Title= models.CharField(max_length=100)
    Title_link=models.URLField()
    Image=models.ImageField(upload_to="/Image")
    Date=models.DateTimeField(auto_now_add=True)
    Summary=models.TextField()
    Content=models.TextField()
    Field1=models.TextField()
    
    # Other fields as needed

