

COPY Artist (artistID, artists)
FROM '/PATH/TO/DIS-PROJEKT-MAIN/artist.csv'
DELIMITER ','
CSV HEADER;


COPY Album (albumID, album_name, artistID)
FROM '/PATH/TO/DIS-PROJEKT-MAIN/album.csv'
DELIMITER ','
CSV HEADER;


COPY Genre (genreID, genreName)
FROM '/PATH/TO/DIS-PROJEKT-MAIN/genre.csv'
DELIMITER ','
CSV HEADER;


COPY Mood (moodID, MoodName)
FROM '/PATH/TO/DIS-PROJEKT-MAIN/mood.csv'
DELIMITER ','
CSV HEADER;


COPY Track (trackID, track_name, albumID, artistID, moodID, genreID, popularity, duration_ms, explicit, danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, valence, tempo, time_signature)
FROM '/PATH/TO/DIS-PROJEKT-MAIN/track.csv'
DELIMITER ','
CSV HEADER;

