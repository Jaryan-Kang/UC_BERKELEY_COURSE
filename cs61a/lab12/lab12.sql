CREATE TABLE finals AS
  SELECT "RSF" AS hall, "61A" as course UNION
  SELECT "Wheeler"    , "61A"           UNION
  SELECT "Pimentel"   , "61A"           UNION
  SELECT "Li Ka Shing", "61A"           UNION
  SELECT "Stanley"    , "61A"           UNION
  SELECT "RSF"        , "61B"           UNION
  SELECT "Wheeler"    , "61B"           UNION
  SELECT "Morgan"     , "61B"           UNION
  SELECT "Wheeler"    , "61C"           UNION
  SELECT "Pimentel"   , "61C"           UNION
  SELECT "Soda 310"   , "61C"           UNION
  SELECT "Soda 306"   , "10"            UNION
  SELECT "RSF"        , "70";

CREATE TABLE sizes AS
  SELECT "RSF" AS room, 900 as seats    UNION
  SELECT "Wheeler"    , 700             UNION
  SELECT "Pimentel"   , 500             UNION
  SELECT "Li Ka Shing", 300             UNION
  SELECT "Stanley"    , 300             UNION
  SELECT "Morgan"     , 100             UNION
  SELECT "Soda 306"   , 80              UNION
  SELECT "Soda 310"   , 40              UNION
  SELECT "Soda 320"   , 30;

CREATE TABLE big AS
  SELECT course
  FROM finals
  JOIN sizes ON finals.hall = sizes.room
  GROUP BY course
  HAVING SUM(seats) >= 1000;

CREATE TABLE remaining AS
SELECT course,
       SUM(seats) - MAX(seats) AS remaining
FROM (
    SELECT f.course, s.seats
    FROM finals f
    JOIN sizes s ON f.hall = s.room
) AS course_seats
GROUP BY course;


CREATE TABLE sharing AS
SELECT finals.course,
       COUNT(DISTINCT finals.hall) AS shared
FROM finals
JOIN (
    SELECT hall
    FROM finals
    GROUP BY hall
    HAVING COUNT(DISTINCT course) > 1
) shared_halls ON finals.hall = shared_halls.hall
GROUP BY finals.course;


CREATE TABLE pairs AS
SELECT
    sizes1.room || ' and ' || sizes2.room || ' together have ' || (sizes1.seats + sizes2.seats) || ' seats' AS rooms
FROM sizes sizes1
JOIN sizes sizes2 ON sizes1.room < sizes2.room
WHERE sizes1.seats + sizes2.seats >= 1000
ORDER BY (sizes1.seats + sizes2.seats) DESC;


