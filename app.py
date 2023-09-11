from email.mime import image
from select import select
import streamlit as st 
import pickle 
import pandas as pd
import requests
import json
import gzip

def fetch_description(movie_name):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey=358825ee"
    movie =requests.get(url).text
    movies_dict= json.loads(movie)
    text = movies_dict['Plot']
    return text

def fetch_poster(movie_name):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey=358825ee"
    movie =requests.get(url).text
    movies_dict= json.loads(movie)
    poster = movies_dict['Poster']
    return poster

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommend_movie_posters = []
    recommend_text=[]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_poster(movies.iloc[i[0]].title))
        recommend_text.append(fetch_description(movies.iloc[i[0]].title))
    return recommended_movies,recommend_movie_posters,recommend_text

movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl.gz','rb'))

st.title('Movie Recommendation App')

selected_movie_name = st.selectbox(
    'Select a Movie',
    movies['title'].values)

if st.button('Recommend'):
    names,posters,texts= recommend(selected_movie_name)
    
    tab1, tab2, tab3,tab4,tab5 = st.tabs(names)
    
    with tab1:
        st.header(names[0])
        st.image(posters[0], width=200)
        st.subheader("Plot")
        st.write(texts[0])
        
    with tab2:
        st.header(names[1])
        st.image(posters[1], width=200)
        st.subheader("Plot")
        st.write(texts[1])
    with tab3:
        st.header(names[2])
        st.image(posters[2], width=200)
        st.subheader("Plot")
        st.write(texts[2])
    with tab4:
        st.header(names[3])
        st.image(posters[3], width=200)
        st.subheader("Plot")
        st.write(texts[3])
        
    with tab5:
        st.header(names[4])
        st.image(posters[4], width=200)
        st.subheader("Plot")
        st.write(texts[4])
    