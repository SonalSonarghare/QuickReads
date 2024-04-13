import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances
from scipy.sparse import csr_matrix
from django.db import connection
import django
from django.conf import settings
import os

# Set DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'QuickReads.settings')

# Initialize Django's settings
django.setup()

# Now you can access Django's settings and configure logging
if hasattr(settings, 'LOGGING_CONFIG'):
    # Configure logging if LOGGING_CONFIG is defined
    django.conf.settings.LOGGING_CONFIG = None

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

# Connect to the Django database and fetch user ID
connection.connect()
query = "SELECT id FROM auth_user;"
df_auth_user = pd.read_sql_query(query, connection)

# Check if there are any user IDs available
if not df_auth_user.empty:
    # Take the first user ID
    user_id = df_auth_user.iloc[0]['id']
else:
    st.write("No user IDs found in the database.")
    exit()

# Define Streamlit app
def main():
    st.title("Hybrid Recommendations App")

    # Get recommendations
    top_hybrid_recommendations = get_hybrid_recommendations(user_id)

    # Display recommendations
    if not top_hybrid_recommendations.empty:
        st.write(f"Top {len(top_hybrid_recommendations)} hybrid recommendations for User ID {user_id}:")
        st.write(pd.DataFrame(top_hybrid_recommendations, columns=['Article ID', 'Title', 'Title_link']))
    else:
        st.write("No recommendations found for this user.")


if __name__ == "__main__":
    main()
