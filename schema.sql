CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mood_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    mood1 TEXT NOT NULL,
    mood2 TEXT NOT NULL,
    mood3 TEXT NOT NULL,
    challenge_completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS mood_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood_state TEXT NOT NULL,
    response_type TEXT NOT NULL,
    content TEXT NOT NULL
);