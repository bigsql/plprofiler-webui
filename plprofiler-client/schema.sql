DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS databases;

CREATE TABLE users (
  uid INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  PASSWORD TEXT NOT NULL
);

CREATE TABLE databases (
  host TEXT NOT NULL,
  port INTEGER NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY(host, port, name)
);
