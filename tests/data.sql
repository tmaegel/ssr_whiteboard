INSERT INTO table_users(name, password)
VALUES
  ('admin', '$2a$10$Q0X4lrRRIvWoLFoiX3CvAO/8fesQsnMR.tQxyBYjzuoSSm4W9IFKe'),
  ('test1', '$2a$10$Q0X4lrRRIvWoLFoiX3CvAO/8fesQsnMR.tQxyBYjzuoSSm4W9IFKe'),
  ('test2', '$2a$10$Q0X4lrRRIvWoLFoiX3CvAO/8fesQsnMR.tQxyBYjzuoSSm4W9IFKe');

INSERT INTO table_workout(userId, name, description, datetime)
VALUES
  (1, 'Workout A from admin', 'Workout A description from admin', 0),
  (1, 'Workout B from admin', 'Workout B description from admin', 0),
  (2, 'Workout A from test1', 'Workout A description from test1', 0),
  (2, 'Workout B from test1', 'Workout B description from test1', 0),
  (3, 'Workout A from test2', 'Workout A description from test2', 0),
  (3, 'Workout B from test2', 'Workout B description from test2', 0);


INSERT INTO table_workout_score(userId, workoutId, score, rx, datetime, note)
VALUES
  (1, 1, 80, 1, 1604825807, 'note for workout A from admin'),
  (2, 3, 100, 1, 1604825807, 'note for workout A from test1'),
  (2, 3, 120, 1, 1604925807, 'note for workout A from test1'),
  (2, 4, 140, 0, 1604925807, 'note for workout B from test1');

INSERT INTO table_equipment(equipment)
VALUES
  ('Equipment 1'),
  ('Equipment 2'),
  ('Equipment 3');

INSERT INTO table_movements(movement, equipmentIds)
VALUES
  ('Movement 1', 1),
  ('Movement 2', 1),
  ('Movement 3', 2);
