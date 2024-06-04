

COPY Artist (artistID, artists)
FROM '/Users/gooni/Desktop/DIS PROJECT 2024/artist.csv'
DELIMITER ','
CSV HEADER;


COPY Album (albumID, album_name, artistID)
FROM '/Users/gooni/Desktop/DIS PROJECT 2024/clean_album.csv'
DELIMITER ','
CSV HEADER;


COPY Genre (genreID, genreName)
FROM '/Users/gooni/Desktop/DIS PROJECT 2024/genre.csv'
DELIMITER ','
CSV HEADER;


COPY Mood (moodID, MoodName)
FROM '/Users/gooni/Desktop/DIS PROJECT 2024/mood.csv'
DELIMITER ','
CSV HEADER;


COPY Track (trackID, track_name, albumID, artistID, moodID, genreID, popularity, duration_ms, explicit, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature)
FROM '/Users/gooni/Desktop/DIS PROJECT 2024/track.csv'
DELIMITER ','
CSV HEADER;

