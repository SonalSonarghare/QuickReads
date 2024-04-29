from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from base.models import Article, Bookmark,Like
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
    articles = Article.objects.filter(Category='Health')[:12]
    return render(request, "Health.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#BUISNESS
@login_required(login_url='Login')
def Business(request):
    articles = Article.objects.filter(Category='Business')[:12]
    return render(request, "Business.html", {'articles': articles})
def Try(request):
    return render(request, "try.html")

#SPORTS
@login_required(login_url='Login')
def Sports(request):
    articles = Article.objects.filter(Category='Sports')[:12]
    return render(request, "Sports.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#TECHNOLOGY
@login_required(login_url='Login')
def Technology(request):
    articles = Article.objects.filter(Category='Technology')[:12]
    return render(request, "Technology.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#EDUCATION
@login_required(login_url='Login')
def Education(request):
    articles = Article.objects.filter(Category='Education')[:12]
    return render(request, "Education.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#MOVIES
@login_required(login_url='Login')
def Movies(request):
    articles = Article.objects.filter(Category='Movies')[:12]
    return render(request, "Movies.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#POLITICS
@login_required(login_url='Login')
def Politics(request):
    articles = Article.objects.filter(Category='Politics')[:12]
    return render(request, "Politics.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#NATURE
@login_required(login_url='Login')
def Nature(request):
    articles = Article.objects.filter(Category='Nature')[:12]
    return render(request, "Nature.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")

#TRAVEL
@login_required(login_url='Login')
def Travel(request):
    articles = Article.objects.filter(Category='Travel')[:12]
    return render(request, "Travel.html", {'articles': articles})

def Try(request):
    return render(request, "try.html")


#Saved
def saved(request):
    articles=Bookmark.objects.filter(user=request.user)
    return render(request, "saved.html", {'articles': articles})
          
#Bookmark
@login_required
def add_bookmark(request, *args, **kwargs):
    article_pk = kwargs['pk']  # Get the primary key of the article from kwargs
    article = Article.objects.get(pk=article_pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
    return redirect('saved')

@login_required
def remove_bookmark(request, *args, **kwargs):
    article_pk = kwargs['pk']  # Get the primary key of the article from kwargs
    Bookmark.objects.get(user=request.user, pk=article_pk).delete()
    return redirect('saved')
#Like
def like(request):
    articles=Like.objects.filter(user=request.user)
    return render(request, "Like.html", {'articles': articles})
#Like
@login_required
def add_Like(request, *args, **kwargs):
    article_pk = kwargs['pk']  # Get the primary key of the article from kwargs
    article = Article.objects.get(pk=article_pk)
    like, created = Like.objects.get_or_create(user=request.user, article=article)
    article.likes += 1  # Increment the likes count
    article.save()
    return redirect('like')

@login_required
def remove_Like(request, *args, **kwargs):
    article_pk = kwargs['pk']  # Get the primary key of the article from kwargs
    like = Like.objects.get(user=request.user, pk=article_pk)
    article = like.article
    article.likes -= 1  # Decrement the likes count
    article.save()
    like.delete()
    return redirect('like')

       

          
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances
from scipy.sparse import csr_matrix
from datetime import datetime

# Load user interactions and articles data
df_user = pd.read_csv('Scrape/user_interactions.csv', encoding='utf-8-sig')
df_articles = pd.read_csv('Scrape/Final(1).csv', encoding='utf-8-sig')

# Preprocess user interactions data
df_user['Timestamp'] = pd.to_datetime(df_user['Timestamp'], format='%d-%m-%Y %H:%M')
df_user = df_user.sort_values(by='Timestamp', ascending=False)
df_user = df_user.drop_duplicates(subset=['User ID', 'Article_ID', 'Action'])

# Preprocess articles data
df_articles['Date'] = pd.to_datetime(df_articles['Date'])


# Create a TF-IDF vectorizer for article titles and types
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix_title = tfidf_vectorizer.fit_transform(df_articles['Title'])
tfidf_matrix_type = tfidf_vectorizer.fit_transform(df_articles['Type'])

# Compute similarity scores based on article titles
cosine_sim_title = linear_kernel(tfidf_matrix_title, tfidf_matrix_title)
cosine_sim_type = linear_kernel(tfidf_matrix_type, tfidf_matrix_type)

# Normalize interaction scores
scaler = MinMaxScaler()
df_user['Interaction_score'] = scaler.fit_transform(df_user['Action'].map({'view': 1, 'like': 2, 'comment': 3, 'share': 4, 'bookmark': 5}).values.reshape(-1, 1))

# Create user-item interaction matrix
user_item_matrix = df_user.pivot_table(index='User ID', columns='Article_ID', values='Interaction_score', fill_value=0)

# Convert user-item matrix to sparse matrix
sparse_user_item = csr_matrix(user_item_matrix.values)

# Compute user similarity matrix based on interactions
user_similarity = pairwise_distances(sparse_user_item, metric='cosine')

# Collaborative filtering recommendations
def get_collaborative_recommendations(user_id, n=6):
    if user_id not in user_item_matrix.index:
        print(f"User ID {user_id} not found in user_item_matrix.")
        return pd.DataFrame(columns=['Article_ID', 'Title', 'Title_link'])

    user_index = user_item_matrix.index.get_loc(user_id)
    user_similarities = user_similarity[user_index]
    similar_users_indices = np.argsort(user_similarities)[1:n+1]
    similar_users_interactions = user_item_matrix.iloc[similar_users_indices]
    aggregated_scores = similar_users_interactions.sum(axis=0)
    recommended_article_ids = aggregated_scores.nlargest(n).index
    recommended_articles = df_articles[df_articles['Article_ID'].isin(recommended_article_ids)]
    return recommended_articles[['Article_ID', 'Title', 'Title_link']]

# Content-based filtering recommendations
def get_content_based_recommendations(user_id, n=6):
    user_interactions = df_user[df_user['User ID'] == user_id]

    if user_interactions.empty:
        return pd.DataFrame(columns=['Article_ID', 'Title', 'Title_link'])

    viewed_article_ids = user_interactions['Article_ID'].tolist()
    avg_cosine_sim = (cosine_sim_title + cosine_sim_type) / 2.0
    viewed_article_indices = df_articles[df_articles['Article_ID'].isin(viewed_article_ids)].index
    avg_similarities = avg_cosine_sim[viewed_article_indices].mean(axis=0)
    top_indices = np.argsort(avg_similarities)[::-1][:n]
    recommended_article_ids = df_articles.iloc[top_indices]['Article_ID']
    recommended_articles = df_articles[df_articles['Article_ID'].isin(recommended_article_ids)]

    return recommended_articles[['Article_ID', 'Title', 'Title_link']]

# Hybrid recommendations
def get_hybrid_recommendations(user_id, n=7):
    collaborative_recommendations = get_collaborative_recommendations(user_id, n)
    content_based_recommendations = get_content_based_recommendations(user_id, n)
    hybrid_recommendations = pd.merge(collaborative_recommendations, content_based_recommendations, on=['Article_ID','Title', 'Title_link'], how='outer')
    hybrid_recommendations = hybrid_recommendations.drop_duplicates(subset=['Title', 'Title_link'])
    hybrid_recommendations = hybrid_recommendations.merge(df_articles[['Article_ID','Type','Title','Title_link','Image','Date', 'Summary', 'Content', 'Field1']], on=['Article_ID','Title', 'Title_link'], how='left')
    return hybrid_recommendations.values.tolist() 

# Django view function
def my_view(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        top_hybrid_recommendations = get_hybrid_recommendations(user_id)
        print(top_hybrid_recommendations)  # Print the content
        return render(request, 'my_view.html', {'articles': top_hybrid_recommendations})
    else:
        return HttpResponse("User is not authenticated")
    
from django.shortcuts import render

import csv
from datetime import datetime
from django.db import models
from base.models import Article

def load_articles_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row['Category']
            title = row['Title']
            title_link = row['Title_link']
            image = row['Image']
            date = datetime.strptime(row['Date'], '%B %d, %Y')
            summary = row['Summary']
            content = row['Content']
            field1 = row['Field1']
            
            # Create and save Article instance
            article = Article.objects.create(
                Category=category,
                Title=title,
                Title_link=title_link,
                Image=image,
                Date=date,
                Summary=summary,
                Content=content,
                Field1=field1
            )

def csv_forall(request):
    list=[
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Business_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Education_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\healthline_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Movies_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Nature_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Politics_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Sports_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Technology_articles.csv',
        r'C:\Users\Sonal R Sonarghare\article\QuickReads\Scrape\Travel_articles.csv',
        
        
    ]
    
    for i in list:
        load_articles_from_csv(i)

    return HttpResponse("Done.")   


