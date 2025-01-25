import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bd1998ca34780208deb7bfe1b2f2f035"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500" 
    except Exception as e:
        return "https://via.placeholder.com/500" 

movies = pickle.load(open("movie_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("Movie Recommender System")

imageCarouselComponent = components.declare_component(
    "image-carousel-component", 
    path="C:/Users/lenovo/Desktop/MovieRecommender/frontend/frontend/public"
)

imageUrls = [
    fetch_poster(1632), fetch_poster(299536), fetch_poster(17455), fetch_poster(2830),
    fetch_poster(429422), fetch_poster(9722), fetch_poster(13972), fetch_poster(240),
    fetch_poster(155), fetch_poster(598), fetch_poster(914), fetch_poster(255709),
    fetch_poster(572154)
]

if imageCarouselComponent:
    imageCarouselComponent(imageUrls=imageUrls, height=200)

selectvalue = st.selectbox("Select a movie from the dropdown", movies_list)

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
        recommended_movies = []
        recommended_posters = []
        for i in distances[1:6]:  
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_posters
    except Exception as e:
        return [], []

if st.button("Show Recommend"):
    recommended_movies, recommended_posters = recommend(selectvalue)
    if recommended_movies:
        cols = st.columns(5) 
        for col, movie, poster in zip(cols, recommended_movies, recommended_posters):
            with col:
                st.text(movie)
                st.image(poster)
    else:
        st.error("Unable to fetch recommendations. Please try again.")
