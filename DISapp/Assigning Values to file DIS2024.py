import pandas as pd
from flask import Flask,render_template,request

df = pd.read_csv("datasetmusic.csv")
print(df.head())



def get_mood(danceability):
    if danceability >= 0.8:
        return 'very Energetic'
    elif danceability >= 0.6:
        return 'energetic'
    elif danceability >= 0.4:
        return 'neutral'
    elif danceability >= 0.2:
        return 'calm'
    else:
        return 'tired'


df['MoodName'] = df['danceability'].apply(get_mood)


unique_artists = df['artists'].unique()
unique_albums = df['album_name'].unique()
unique_genres = df['track_genre'].unique()
unique_moods = df ["MoodName"].unique()


artist_id_mapping = {artist: idx for idx, artist in enumerate(unique_artists, start=1)}

album_id_mapping ={album: idx for idx, album in enumerate(unique_albums, start=1)}

genre_id_mapping = {genre: idx for idx, genre in enumerate(unique_genres,start=1)}

mood_id_mapping = {mood: idx for idx, mood in enumerate(unique_moods, start=1)}


def get_artistID(artist_name):
    return artist_id_mapping[artist_name]

  
def get_albumID(artist_name):
    return album_id_mapping[artist_name]

def get_genreID(artist_name):
    return genre_id_mapping[artist_name]


def get_moodID(artist_name):
    return mood_id_mapping[artist_name]

df['albumID'] = df['album_name'].apply(get_albumID)

df['artistID'] = df['artists'].apply(get_artistID)

df ['genreID'] = df['track_genre'].apply(get_genreID)

df['moodID'] = df['MoodName'].apply(get_moodID)








print(df['moodID'])

# df.to_csv("MusicDatasetV2.csv",index=False)