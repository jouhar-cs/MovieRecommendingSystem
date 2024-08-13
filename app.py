import streamlit as st
import pickle
import pandas as pd
import requests

# Replace with your actual TMDB API key
TMDB_API_KEY = '8265bd1679663a7ea12ac168da84d2e8'

# Function to fetch movie posters
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US')
        data = response.json()
        if response.status_code == 200 and 'poster_path' in data:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Image"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750.png?text=No+Image"

# Function to recommend movies
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list[1:6]:  # Top 5 recommendations
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the database.")
        return [], []

# Load data from pickle files
movie_dict = pickle.load(open('../movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('../similarity.pkl', 'rb'))

# Add placeholder columns if they do not exist
if 'genres' not in movies.columns:
    movies['genres'] = 'Unknown'
if 'rating' not in movies.columns:
    movies['rating'] = 'Not Rated'

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ['Home', 'Projects', 'Skills', 'Education', 'Contact',
                                     'Movie Search', 'Favorite Movies', 'Random Movie',
                                     'Genre Filter', 'Movie Ratings'])

# Theme Selection
st.sidebar.title("Customization")
theme = st.sidebar.radio('Select Theme', ['Default', 'Green', 'Blue'])

if 'theme' not in st.session_state:
    st.session_state.theme = 'Default'

if theme != st.session_state.theme:
    st.session_state.theme = theme

# Apply theme
if st.session_state.theme == 'Green':
    st.markdown("""
        <style>
            body {
                background-color: #e7f4e4;
                color: #000000;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
elif st.session_state.theme == 'Blue':
    st.markdown("""
        <style>
            body {
                background-color: #e0f7fa;
                color: #000000;
            }
            .stButton>button {
                background-color: #0288d1;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: #FFFFFF;
                color: #000000;
            }
        </style>
    """, unsafe_allow_html=True)

# Animated Header
st.markdown("""
    <style>
        @keyframes slideIn {
            from {
                transform: translateX(-100%);
            }
            to {
                transform: translateX(0);
            }
        }
        .slide-in {
            animation: slideIn 1s ease-out;
        }
    </style>
""", unsafe_allow_html=True)

# Portfolio Title
st.title('Mahammad Ali Jouhar')

if options == 'Home':
    # About Section
    st.header('About Me')
    st.write("""
    Hello! My name is **Mahammad Ali Jouhar**. I am currently pursuing my **Engineering undergraduate degree** in the field of **Computer Science**.

    I am a passionate **web developer** with experience in building applications. 

    I enjoy working on projects that:
    - Utilize data to solve real-world problems.
    - Enhance user experiences.
    - Drive technological innovation.

    In my spare time, I love exploring new technologies and continuously improving my skills.
    """)

elif options == 'Projects':
    # Projects Section
    st.header('Projects')
    st.subheader('Movie Recommender System')
    st.write("""
    This project uses machine learning to recommend movies based on user preferences. 
    Select a movie to receive similar movie suggestions along with their posters.
    """)

    # Recommendation System
    selected_movie_name = st.selectbox(
        'Select a movie to get recommendations:',
        movies['title'].values)

    if st.button('Recommend'):
        with st.spinner('Fetching recommendations...'):
            names, posters = recommend(selected_movie_name)

        # Display recommendations in columns
        if names:
            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.text(names[i])
                    st.image(posters[i])
        else:
            st.error("No recommendations available.")

elif options == 'Movie Search':
    st.header('Search for a Movie')
    search_term = st.text_input("Enter movie name:")
    if search_term:
        filtered_movies = movies[movies['title'].str.contains(search_term, case=False)]
        st.write(filtered_movies[['title', 'movie_id']])

elif options == 'Favorite Movies':
    st.header('Your Favorite Movies')
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    selected_favorite = st.selectbox('Select a movie to add to favorites:', movies['title'].values)
    if st.button('Add to Favorites'):
        st.session_state.favorites.append(selected_favorite)
        st.success(f"{selected_favorite} added to favorites!")

    st.write("Your Favorites:")
    st.write(st.session_state.favorites)

elif options == 'Random Movie':
    st.header('Random Movie Picker')
    random_movie = movies.sample(1)['title'].values[0]
    st.write(f"How about watching **{random_movie}**?")

elif options == 'Genre Filter':
    st.header('Filter by Genre')
    genres = movies['genres'].unique()
    selected_genre = st.selectbox('Select a genre:', genres)
    filtered_movies = movies[movies['genres'].str.contains(selected_genre)]
    st.write(filtered_movies[['title']])

elif options == 'Movie Ratings':
    st.header('Movie Ratings')
    st.write(movies[['title', 'rating']])

elif options == 'Skills':
    # Skills Section
    st.header('Skills & Skill Proficiency')
    skills_proficiency = {
        "Java": 90,
        "Python": 90,
        "Machine Learning": 70,
        "Data Structures": 90,
        "JavaScript": 85,
        "Web Development": 80
    }

    skill_cols = st.columns(6)
    for i, (skill, proficiency) in enumerate(skills_proficiency.items()):
        with skill_cols[i]:
            st.write(f"{skill}")
            st.progress(proficiency)

elif options == 'Education':
    # Education Section
    st.header('Education')
    st.write("""
    - **Bachelor of Technology in Computer Science**, Vishveshwarayya Technological University (Expected Graduation: 2025)
      - Relevant Coursework: Data Structures, Algorithms, Machine Learning, Web Development, Database Systems.
      - Activities: Member of the Coding Club.
    """)

elif options == 'Contact':
    # Contact Section
    st.header('Contact Me')
    st.write("""
    Feel free to reach out via [LinkedIn](https://www.linkedin.com/in/mahammad-ali-jouhar-09a532253) or [Email](mailto:jouharjouhar633@gmail.com) or [GitHub](https://github.com/jouhar-cs).
    """)

    # Contact Form
    st.subheader("Send me a message")
    with st.form("contact_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("Send")

        if submit_button:
            st.success("Message sent!")

# Footer with social media links
st.write("""
---
Created with ❤️ by Mahammad Ali Jouhar
""")

st.markdown("""
    <style>
        .stHeader { font-size: 24px; font-weight: bold; }
        .stText { font-size: 16px; }
        .css-1aumxhk { padding: 20px; }
        .css-1d391kg { font-size: 18px; font-weight: bold; }
        .css-10trblm { font-size: 16px; }
        footer {
            display: flex;
            justify-content: center;
            padding: 10px;
        }
        footer a {
            margin: 0 10px;
            text-decoration: none;
            color: inherit;
        }
    </style>
""", unsafe_allow_html=True)
