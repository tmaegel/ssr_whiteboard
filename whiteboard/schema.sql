DROP TABLE IF EXISTS table_users;
DROP TABLE IF EXISTS table_tags;
DROP TABLE IF EXISTS table_equipment;
DROP TABLE IF EXISTS table_movements;
DROP TABLE IF EXISTS table_workout;
DROP TABLE IF EXISTS table_workout_score;
DROP TABLE IF EXISTS table_workout_tags;

CREATE TABLE table_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  password TEXT
);
CREATE TABLE table_tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER,
  tag TEXT
);
CREATE TABLE table_equipment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  equipment TEXT
);
CREATE TABLE table_movements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  movement TEXT,
  equipmentIds TEXT
);
CREATE TABLE table_workout (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER,
  name TEXT,
  description TEXT,
  datetime INTEGER
);
CREATE TABLE table_workout_score (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userId INTEGER,
  workoutId INTEGER,
  score TEXT,
  rx BOOL,
  datetime INTEGER,
  note TEXT
);
CREATE TABLE table_workout_tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workoutId INTEGER,
  tagId INTEGER
);
