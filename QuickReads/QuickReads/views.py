from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from base.models import Article, Bookmark
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
       
           
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances
from scipy.sparse import csr_matrix
from datetime import datetime

# Load data
df_user = pd.read_csv('C:/Users/Sonal R Sonarghare/article/QuickReads/streamlit_apps/user_interactions_2500_rows.csv', encoding='latin1')
df_articles = pd.read_csv('C:/Users/Sonal R Sonarghare/article/QuickReads/streamlit_apps/Article_data.csv', encoding='latin1')

# Create TF-IDF vectorizer for article titles
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix_title = tfidf_vectorizer.fit_transform(df_articles['Title'])

# Compute similarity scores based on article titles
cosine_sim_title = linear_kernel(tfidf_matrix_title, tfidf_matrix_title)

# Normalize interaction scores
scaler = MinMaxScaler()
df_user['Interaction_score'] = scaler.fit_transform(df_user['Action'].map({'view': 1, 'like': 2, 'comment': 3, 'share': 4, 'bookmark': 5}).values.reshape(-1, 1))

# Create user-item interaction matrix
user_item_matrix = df_user.pivot_table(index='User ID', columns='Article ID', values='Interaction_score', fill_value=0)

# Convert user-item matrix to sparse matrix
sparse_user_item = csr_matrix(user_item_matrix.values)

# Compute user similarity matrix based on interactions
user_similarity = pairwise_distances(sparse_user_item, metric='cosine')

# Placeholder function for collaborative recommendations
def get_collaborative_recommendations(user_id, n=6):
    user_index = user_item_matrix.index.get_loc(user_id)
    user_similarities = user_similarity[user_index]
    similar_users_indices = np.argsort(user_similarities)[1:n+1]
    similar_users_interactions = user_item_matrix.iloc[similar_users_indices]
    aggregated_scores = similar_users_interactions.sum(axis=0)
    recommended_article_ids = aggregated_scores.nlargest(n).index
    recommended_articles = df_articles[df_articles['Article ID'].isin(recommended_article_ids)]
    return recommended_articles[['Article ID', 'Title', 'Title_link']]

# Function to get content-based recommendations
def get_content_based_recommendations(user_id, n=6):
    user_interactions = df_user[df_user['User ID'] == user_id]
    viewed_articles = user_interactions[user_interactions['Action'] == 'view']
    viewed_article_ids = viewed_articles['Article ID'].tolist()

    if len(viewed_article_ids) == 0:
        return df_articles.sample(n=n)[['Article ID', 'Title', 'Title_link']]

    viewed_article_indices = df_articles[df_articles['Article ID'].isin(viewed_article_ids)].index
    similar_articles_scores = cosine_sim_title[viewed_article_indices].sum(axis=0)
    similar_articles_indices = np.argsort(similar_articles_scores)[::-1]
    recommended_article_ids = [df_articles.iloc[i]['Article ID'] for i in similar_articles_indices if df_articles.iloc[i]['Article ID'] not in viewed_article_ids][:n]
    recommended_articles = df_articles[df_articles['Article ID'].isin(recommended_article_ids)]
    return recommended_articles[['Article ID', 'Title', 'Title_link']]

# Function to get hybrid recommendations combining collaborative and content-based
def get_hybrid_recommendations(user_id, n=6):
    collaborative_recommendations = get_collaborative_recommendations(user_id, n)
    content_based_recommendations = get_content_based_recommendations(user_id, n)

    hybrid_recommendations = pd.merge(collaborative_recommendations, content_based_recommendations, on=['Title', 'Title_link'], how='outer')
    hybrid_recommendations = hybrid_recommendations.drop_duplicates(subset=['Title', 'Title_link']).head(n)

    # Add 'Article ID' column to the recommendations DataFrame
    hybrid_recommendations = hybrid_recommendations.merge(df_articles[['Article ID', 'Title', 'Title_link']], on=['Title', 'Title_link'], how='left')

    return hybrid_recommendations[['Article ID', 'Title', 'Title_link']]

# Define Django view
def Hybrid(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', None)
        if user_id is not None:
            try:
                user_id = int(user_id)
            except ValueError:
                return HttpResponse("Please enter a valid User ID (integer).")

            # Get recommendations
            top_hybrid_recommendations = get_hybrid_recommendations(user_id)

            # Display recommendations
            if not top_hybrid_recommendations.empty:
                context = {
                    'user_id': user_id,
                    'recommendations': top_hybrid_recommendations.to_html(index=False)
                }
                return render(request, 'hybrid_recommendations.html', context)
            else:
                return HttpResponse("No recommendations found for this user.")
        else:
            return HttpResponse("Please provide a User ID.")
    else:
        return HttpResponse("Invalid request method.")           
    


    
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