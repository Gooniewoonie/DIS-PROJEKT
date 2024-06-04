
CREATE TABLE  Artist (
	artistID INT PRIMARY KEY,
	artists VARCHAR(255)
	
);

CREATE TABLE Album (
	albumID INT PRIMARY KEY,
	album_name VARCHAR(255),
	artistID INT,
	FOREIGN KEY (artistID) REFERENCES Artist(artistID)
);

CREATE TABLE Genre (
	genreID INT PRIMARY KEY,
	genreName VARCHAR(255)
);

CREATE TABLE Mood (
	moodID INT PRIMARY KEY,
	MoodName VARCHAR(255)
);

CREATE TABLE Track (
	trackID INT PRIMARY KEY,
	track_name VARCHAR(255),
	albumID INT,
	artistID INT,
	moodID INT,
	popularity INT,
	genreID INT,
    duration_ms INT,
    explicit BOOLEAN,
    danceability FLOAT,
    energy FLOAT,
    loudness FLOAT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    time_signature INT,
	FOREIGN KEY (albumID) REFERENCES Album(albumID),
	FOREIGN KEY (moodID) REFERENCES Mood(moodID),
	FOREIGN KEY (artistID) REFERENCES Artist(artistID),
	FOREIGN KEY (genreID) REFERENCES Genre(genreID)
);

CREATE TABLE BronzeUser (
	B_userID INT PRIMARY KEY,
	risk_type boolean default FALSE,
	password VARCHAR(120),
	name VARCHAR(60)
);

CREATE TABLE SilverUser (
	S_userID INT PRIMARY KEY,
	risk_type boolean default FALSE,
	password VARCHAR(120),
	name VARCHAR(60)
);

CREATE TABLE GoldUser (
	G_userID INT PRIMARY KEY,
	risk_type boolean default FALSE,
	password VARCHAR(120),
	name VARCHAR(60)
);

CREATE TABLE FreeUser (
	F_userID INT PRIMARY KEY,
	risk_type boolean default FALSE,
	password VARCHAR(120),
	name VARCHAR(60)
);


CREATE TABLE Admins (
	A_userID INT PRIMARY KEY,
	risk_type boolean default FALSE,
	password VARCHAR(120),
	name VARCHAR(60)
);

CREATE TABLE Accounts (
	accountID SERIAL PRIMARY KEY,
	created_date date,
	F_userID INT,
    B_userID INT,
    S_userID INT,
    G_userID INT,
    A_userID INT,
	FOREIGN KEY (F_userID) REFERENCES FreeUser(F_userID),
	FOREIGN KEY (B_userID) REFERENCES BronzeUser(B_userID),
	FOREIGN KEY (S_userID) REFERENCES SilverUser(S_userID),
	FOREIGN KEY (G_userID) REFERENCES GoldUser(G_userID),
	FOREIGN KEY (A_userID) REFERENCES Admins(A_userID)
);

CREATE TABLE Danceability (
    trackID INT,
    danceability FLOAT,
    PRIMARY KEY (trackID),
    FOREIGN KEY (trackID) REFERENCES Track(trackID)
);
