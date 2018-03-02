CREATE TABLE redline_poly (poly_id SERIAL PRIMARY KEY, gid int, holc_grade_b varchar(10), holc_grade_a varchar(10), geom geometry);

INSERT INTO redline_poly (gid, holc_grade_b, holc_grade_a, geom)


SELECT
  b.gid, ROW_NUMBER() OVER (ORDER BY b.gid), b.holc_grade as holc_a, a.holc_grade as holc_b, ST_Intersection(ST_Buffer(a.geom, .00001), b.geom)
FROM 
  redline a, redline b  
WHERE 
  a.holc_grade = 'A' AND b.holc_grade != 'A' AND
  ST_Intersects(ST_Buffer(a.geom, .00001), b.geom);


#http://lists.osgeo.org/pipermail/postgis-users/2011-May/029562.html
