CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE songs (
    song_id VARCHAR(255) PRIMARY KEY,
    title TEXT,  
    artist TEXT   
);

CREATE TABLE play_history (
    play_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id),
    song_id VARCHAR(255) REFERENCES songs(song_id),
    play_count INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON play_history (user_id);
CREATE INDEX ON play_history (song_id);