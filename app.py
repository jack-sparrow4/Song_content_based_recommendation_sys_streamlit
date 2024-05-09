import streamlit as st
import pickle
import pandas as pd
import requests
import http.client
import json

conn = http.client.HTTPSConnection("saavn.dev")


def fetch_poster(music_title):
    #print('here', music_title)
    music_title = music_title.replace(" ", "%20")
    response = requests.get("https://saavn.dev/api/search/songs?query={}&page=1&limit=2".format(music_title))
    #print("response", response)
    data = response.json()
    #print(data)
    # conn.request(f"GET", "/api/search/songs?query={music_title}&page=1&limit=1")
    # data = json.loads(conn.getresponse().read().decode('utf-8'))
    #print("Response", data)
    return data['data']['results'][0]['image'][2]['url']


def recommend(musics):
    music_index = music[music['Song-Name'] == musics].index[0]
    distances = similarity[music_index]
    music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_music = []
    recommended_music_poster = []
    for i in music_list:
        music_title = music.iloc[i[0]]
        recommended_music.append(music_title['Song-Name'])
        recommended_music_poster.append(fetch_poster(music_title['Song-Name']))
    return recommended_music, recommended_music_poster

def recommend_based_on_genre(genre, songs_info):
    filtered_songs = songs_info[songs_info['Genre'] == genre].sort_values(by='User_Rating_num', ascending=False).head(5)
    print("filtered_songs", filtered_songs)
    return filtered_songs['Song-Name'].tolist()

music_dict = pickle.load(open(r'F:\scaler\music_recommendation_system_streamlt\music_data.pkl', 'rb'))
music = pd.DataFrame(music_dict)

initial_dict = pickle.load(open(r'F:\scaler\music_recommendation_system_streamlt\song_data_initial.pkl','rb'))
songs_info = pd.DataFrame(initial_dict)
print("songs dictionay", songs_info.columns)

similarity = pickle.load(open(r'F:\scaler\music_recommendation_system_streamlt\similarities.pkl', 'rb'))
st.title('Song Recommendation System')

selected_music_name = st.selectbox('Select a song you like', music['Song-Name'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_music_name)

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


selected_genre = st.selectbox('Select the genre you like', songs_info['Genre'].unique())

if st.button('Genre top songs'):
    songs = recommend_based_on_genre(selected_genre, songs_info)
    #print("songs", songs)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(songs[0])
        st.image(fetch_poster(songs[0]))
    with col2:
        st.text(songs[1])
        st.image(fetch_poster(songs[1]))
    with col3:
        st.text(songs[2])
        st.image(fetch_poster(songs[2]))
    with col4:
        st.text(songs[3])
        st.image(fetch_poster(songs[3]))
    with col5:
        st.text(songs[4])
        st.image(fetch_poster(songs[4]))