import streamlit as st
import pickle
import pandas as pd
import requests


# Function to fetch poster of a movie
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=1c9d4a5634ece2693fe47d87a2bd513f&&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


# Function to fetch movie details (overview, cast, crew)
def fetch_movie_details(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=1c9d4a5634ece2693fe47d87a2bd513f&language=en-US')
    movie_data = response.json()

    # Fetching overview
    overview = movie_data['overview']

    # Fetching cast
    cast_response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=1c9d4a5634ece2693fe47d87a2bd513f&language=en-US')
    cast_data = cast_response.json()
    cast = [cast_member['name'] for cast_member in cast_data['cast'][:5]]  # Top 5 cast members

    # Fetching crew
    crew = [crew_member['name'] for crew_member in cast_data['crew'][:5]]  # Top 5 crew members

    return overview, cast, crew


# Function to recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load movies data and similarity matrix
movies_dict = pickle.load(open(r"C:\Users\Admin\PycharmProjects\MovRecSys\.venv\movie_dict.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(r"C:\Users\Admin\PycharmProjects\MovRecSys\.venv\similarity.pkl", 'rb'))

# Streamlit UI setup
st.title("AI-Powered Movie Recommendation System")

# Movie selection dropdown
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

# When the user presses the 'Recommend' button
if st.button('Recommend'):
    # Get movie details
    movie_id = movies[movies['title'] == selected_movie_name].iloc[0].id
    overview, cast, crew = fetch_movie_details(movie_id)

    # Display the selected movie's poster
    movie_poster = fetch_poster(movie_id)
    st.image(movie_poster, caption=selected_movie_name, use_container_width=True)

    # Display movie overview, cast, and crew
    st.subheader('Movie Overview:')
    st.write(overview)

    st.subheader('Top Cast:')
    st.write(", ".join(cast))

    st.subheader('Top Crew:')
    st.write(", ".join(crew))
    st.title("Recommended Movies for your choice")
    # Get recommended movies
    names, posters = recommend(selected_movie_name)

    # Display recommended movies in columns
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