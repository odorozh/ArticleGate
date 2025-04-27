CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    affiliation_org_id INTEGER,
    FOREIGN KEY (affiliation_org_id) REFERENCES organisation (id)
);

CREATE TABLE IF NOT EXISTS article (
    doi TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    posting_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS article_to_author (
    doi TEXT NOT NULL,
    author_id INTEGER,
    place INTEGER NOT NULL CHECK (place > 0),
    FOREIGN KEY (author_id) REFERENCES author (id)
);

CREATE TABLE IF NOT EXISTS organisation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT
);
