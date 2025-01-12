import requests
import streamlit as st
import pickle
import pandas as pd


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_overview = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_overview.append(movies.iloc[i[0]].tags)
    return recommended_movies, recommended_movies_posters, recommended_movies_overview


# Load data
movies_dict = pickle.load(open(
    r'C:/Users/SAHIL/OneDrive/Documents/Projects/Machine Learning/Movie Recommendation System/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(
    "C:/Users/SAHIL/OneDrive/Documents/Projects/Machine Learning/Movie Recommendation System/similarity.pkl", 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System 🍿')

st.markdown("""
<style>
body {
    background-color: #f0f2f6;
}
h1 {
    color: #ff4b4b;
    text-align: center;
}
.movie-title {
    font-size: 21px;
    font-weight: bold;
    color: #F5F5F5;
    margin-bottom: 5px;
}
.movie-overview {
    font-size: 15px;
    color: #E8E8E8;
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Select a movie you like:",
    movies['title'].values)

if st.button("Recommend"):
    names, posters, overviews = recommend(selected_movie_name)

    st.subheader("Recommended Movies:")
    for name, poster, overview in zip(names, posters, overviews):
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(poster, use_column_width=True)
            with col2:
                st.markdown(
                    f'<div class="movie-title">{name}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="movie-overview">{overview}</div>', unsafe_allow_html=True)
