
from django.db import models
from django.contrib.auth.models import User
    
class Article(models.Model):
    '''CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('business', 'Business'),
        ('sports', 'Sports'),
        # Add other categories as needed
    ]'''
    Category = models.TextField()
    Title= models.CharField(max_length=100)
    Title_link=models.URLField()
    Image=models.URLField()
    Date=models.DateTimeField()
    Summary=models.TextField()
    Content=models.TextField()
    Field1=models.TextField()
    likes = models.IntegerField(default=10)
    
    # Other fields as needed

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
