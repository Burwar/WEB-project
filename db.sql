CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
url text NOT NULL,
type text NOT NULL,
text text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name1 text NOT NULL,
name2 text NOT NULL,
name3 text NOT NULL,
sex text NOT NULL,
tel text NOT NULL,
email text NOT NULL,
login text NOT NULL,
password text NOT NULL,
avatar BLOB DEFAULT NULL
);