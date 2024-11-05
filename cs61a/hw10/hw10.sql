CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT child 
  FROM parents 
  JOIN dogs ON parents.parent = dogs.name 
  ORDER BY dogs.height DESC;



-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT dogs.name, sizes.size
  FROM dogs
  JOIN sizes ON dogs.height > sizes.min AND dogs.height <= sizes.max;



-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child as first, b.child as second from parents as a, parents as b where a.parent=b.parent and a.child<b.child;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || first || " and " || second || ", have the same size: " || a.size from size_of_dogs as a, size_of_dogs as b, siblings 
    where a.name=first and b.name=second and a.size = b.size;


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE low_variance AS
  SELECT dogs.fur, MAX(dogs.height) - MIN(dogs.height) AS height_variance
  FROM dogs
  JOIN (SELECT fur, AVG(height) AS average_height FROM dogs GROUP BY fur) AS fur_avgs
    ON dogs.fur = fur_avgs.fur
  GROUP BY dogs.fur
  HAVING SUM(CASE WHEN dogs.height BETWEEN fur_avgs.average_height * 0.7 AND fur_avgs.average_height * 1.3 THEN 1 ELSE 0 END) = COUNT(dogs.fur);

