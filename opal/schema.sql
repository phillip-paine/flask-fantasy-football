DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS teams_strength;
DROP TABLE IF EXISTS seasons;

CREATE TABLE teams (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  season INTEGER NOT NULL,
  season_id INTEGER NOT NULL

);

CREATE TABLE teams_strength (
  name TEXT PRIMARY KEY,
  season TEXT NOT NULL,
  att_coef DOUBLE NOT NULL,
  def_coef DOUBLE NOT NULL
);

CREATE TABLE seasons (
  season INTEGER PRIMARY KEY,
  promoted_1 TEXT NOT NULL,
  promoted_2 TEXT NOT NULL,
  promoted_3 TEXT NOT NULL,
  relegated_1 TEXT NOT NULL,
  relegated_2 TEXT NOT NULL,
  relegated_3 TEXT NOT NULL
);