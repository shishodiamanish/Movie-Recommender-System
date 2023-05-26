import streamlit as st
import pickle
import requests
import sqlite3
import pandas as pd
from streamlit_lottie import st_lottie



st.set_page_config(page_title="Movie Recommender System")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")
#
# -- LOAD ASSETS--
lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_txl2z41u.json")

st_lottie(lottie_coding, height=400, key="coding")


# Data Base Management System

conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
    conn.commit()
def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

def main():
    st.sidebar.title("Login")
    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox(' ', menu)

    if choice == "Home":
        st.sidebar.subheader("Home")

    elif choice == "Login":

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            # if username == "maanshishodia" and password == "Manish@123":
            create_usertable()
            result = login_user(username, password)
            if result:
                st.sidebar.success("Logged in as {}".format(username))

    elif choice == "SignUp":
        st.sidebar.subheader("Create New Account")

        new_user = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("SignUp"):
            create_usertable()
            add_userdata(new_user, new_password)
            st.sidebar.success("You have successfully created an account")
            st.sidebar.info("Go to Login Menu to login")

if __name__ == "__main__":
    main()
    user_result = view_all_users()
    clean_db = pd.DataFrame(user_result, columns=["Username", "Password"])
    clean_db.to_csv()
    pass


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9451f20de59a2418aa812f27637be7ee&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies.title == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster of movie from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(

    'Select the movie you want?',

    movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
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

with st.container():
    st.write("------")
    st.header("Get in touch with me!")
    st.write("##")

contact_form = '''
<form action="https://formsubmit.co/shishodia525@gmail.com" method="POST">
    <input type="Hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your Name" required>
     <input type="email" name="email" placeholder="Your Email" required>
     <textarea name="message" placeholder="Your Message Here" required></textarea>
     <button type="submit">Send</button>
</form>'''

left_column, right_column = st.columns(2)
with left_column:
    st.markdown(contact_form, unsafe_allow_html=True)
with right_column:
    st.empty()

lottie_last_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_aptscmnx.json")

st_lottie(lottie_last_coding, height=200, key="web")

