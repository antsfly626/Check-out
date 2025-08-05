#!/usr/bin/env python
# coding: utf-8

# **Importing libraries**

# In[42]:


import pandas as pd
import numpy as np
import os 
import matplotlib.pyplot as plt
import seaborn as sns
import ast


# In[43]:


filename = "data/Book_Details.csv"
df = pd.read_csv(filename)


# In[44]:


# print info
print(df.shape)
print(df.head(10))
print(df.columns)
print(df.info())
print(df.isnull().sum())
print(df.dtypes)


# In[45]:


# select features
df = df.drop(columns=['format', 'authorlink', 'num_reviews', 'rating_distribution'])

# Sort by num_ratings 
df['num_ratings'] = pd.to_numeric(df['num_ratings'], errors='coerce')
df = df.dropna(subset=['num_ratings'])
# Get top 5000
df = df.sort_values(by='num_ratings', ascending=False).head(5000).reset_index(drop=True)

# format data
df['publication_info'] = df['publication_info'].apply(lambda x: ast.literal_eval(x)[0] if isinstance(x, str) and x.startswith("['") else x)
df['publication_info'] = df['publication_info'].str.replace('^First published ', '', regex=True)

df = df.dropna(subset=['num_pages'])
def safe_num_pages(x):
    if isinstance(x, str):
        try:
            parsed = ast.literal_eval(x)
            if isinstance(parsed, list) and len(parsed) > 0:
                return int(parsed[0])
        except Exception:
            return np.nan
    elif pd.isna(x):
        return np.nan
    else:
        try:
            return int(x)
        except Exception:
            return np.nan

df['num_pages'] = df['num_pages'].apply(safe_num_pages)
df['num_pages'] = df['num_pages'].astype('Int64')  # pandas nullable integer dtype

df['genres'] = df['genres'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)




# In[46]:


from sklearn.feature_extraction.text import TfidfVectorizer
import json

# --- TF-IDF setup ---
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)

# Clean book_details column and reindex
df['book_details'] = df['book_details'].fillna('')
df = df.reset_index(drop=True)

# Fit and transform
tfidf_matrix = vectorizer.fit_transform(df['book_details'])

# Convert sparse matrix to list of vectors
vectors = [tfidf_matrix[i].toarray()[0] for i in range(tfidf_matrix.shape[0])]

# Add new column to df
df = df.reset_index(drop=True)  # just to be safe
df['vector'] = vectors

# Build book data list
book_data = []
for idx, row in df.iterrows():
    vector = tfidf_matrix[idx].toarray()[0].tolist()  # Convert sparse vector to list
    book_data.append({
        'book_title': row['book_title'],
        'book_details': row['book_details'],
        'num_pages': int(row['num_pages']) if not pd.isna(row['num_pages']) else None,
        'publication_info': row['publication_info'],
        'genres': row['genres'],
        'book_id': row['book_id'],
        'author': row['author'],
        'average_rating': row['average_rating'],
        'num_ratings': row['num_ratings'],
        'cover_image_uri': row['cover_image_uri'],
        'vector': vector
    })

# Save vector data to JSON
with open('book_data.json', 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=2)


# In[47]:


# check formatting
features = df.columns
print(features)
print(df.head(5))


# **Compute User Vector**

# In[48]:


def compute_user_vector(user_about_me, liked_book_vectors, vectorizer):
    # Vectorize 'about me' text
    user_vec = vectorizer.transform([user_about_me]).toarray()[0]

    if liked_book_vectors:
        liked_avg = np.mean(liked_book_vectors, axis=0)
        combined_vec = 0.5 * user_vec + 0.5 * liked_avg  
    else:
        combined_vec = user_vec

    return combined_vec


# In[49]:


# reccomenadtion function
from sklearn.metrics.pairwise import cosine_similarity


def recommend_books(user_vec, books_df, filters):
    # Filter books by genre overlap and page range
    def genre_match(book_genres):
        return bool(set(book_genres) & set(filters['genres']))

    filtered = books_df[
        books_df['genres'].apply(genre_match) &
        (books_df['num_pages'] >= filters['min_pages']) &
        (books_df['num_pages'] <= filters['max_pages'])
    ].copy()

    if filtered.empty:
        return pd.DataFrame()  # no matches

    # Prepare matrix of book vectors
    book_vecs = np.vstack(filtered['vector'].values)

    # Compute cosine similarity
    sims = cosine_similarity([user_vec], book_vecs)[0]

    filtered['similarity'] = sims

    # Return top recommendations sorted by similarity
    return filtered.sort_values('similarity', ascending=False)


# In[50]:


# If genres are already lists
from itertools import chain

all_genres = sorted(set(chain.from_iterable(df['genres'])))

# To view them sorted
print(all_genres)


# In[52]:


# Example user input:
user_about_me = "I wanna read something very scary that will keep me up at night. I like horror specifically psychological horror and thrillers."
liked_books_vectors = [book_data[10]['vector'], book_data[25]['vector']]  # example liked books vectors


filters = {
    'genres': all_genres,  # default: include all
    'min_pages': 0,
    'max_pages': 10000
}

user_vec = compute_user_vector(user_about_me, liked_books_vectors, vectorizer)
recommendations = recommend_books(user_vec, df, filters)

print(recommendations[['book_title', 'genres', 'similarity']].head(10))


# In[53]:


# Assuming your vectorizer is named 'vectorizer' and your df has a 'vector' column
# Convert NumPy arrays in 'vector' column to lists
df['vector'] = df['vector'].apply(lambda x: x.tolist() if hasattr(x, 'tolist') else x)


# 1. Export book data (metadata + vector)
book_data_export = df[['book_title', 'book_details', 'num_pages', 'genres', 'vector']].to_dict(orient='records')
with open('book_data.json', 'w', encoding='utf-8') as f:
    json.dump(book_data_export, f, ensure_ascii=False, indent=2)

# 2. Export vocabulary of your TF-IDF vectorizer
# Convert keys and values to native Python types (str and int)
vocab_clean = {str(k): int(v) for k, v in vectorizer.vocabulary_.items()}

with open('tfidf_vocab.json', 'w', encoding='utf-8') as f:
    json.dump(vocab_clean, f, ensure_ascii=False, indent=2)

# 3. Export unique genres (for filters)
from itertools import chain
unique_genres = sorted(set(chain.from_iterable(df['genres'])))
with open('unique_genres.json', 'w', encoding='utf-8') as f:
    json.dump(unique_genres, f, ensure_ascii=False, indent=2)

print(" Exported JSON files: book_data.json, tfidf_vocab.json, unique_genres.json")