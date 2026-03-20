import streamlit as st
import pickle
import pandas as pd
import requests


# page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.write("App started successfully")

# load data
movies = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies)

similarity = pickle.load(open('similarity.pkl','rb'))

# TMDB API KEY
API_KEY = "52d41d87ea9e0823f4b869d3cb9d6ce4"


# fetch poster function
def fetch_poster(id):

    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url).json()

    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# recommendation function
def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        id = movies.iloc[i[0]].id   # ✅ FIX HERE

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(id))

    return recommended_movies, recommended_posters


# title
st.title("🎬 AI Movie Recommendation System")

st.write("Select a movie and get similar movie recommendations with posters")

# movie dropdown
selected_movie = st.selectbox(
    "Choose a movie",
    movies['title'].values
)

# recommend button
if st.button('Recommend Movies'):

    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])