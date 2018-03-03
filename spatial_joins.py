#Create spatial join of census percent black data
CREATE TABLE Census_Black_1990 (poly_id int, pct_black float8, holc_grade varchar(10), geom geometry);

INSERT INTO Census_Black_1990 (poly_id, pct_black, holc_grade, geom)
SELECT redline_poly.poly_id, avg(c.pct_black) AS pct_black, redline_poly.holc_grade_b, redline_poly.geom 
FROM (SELECT c90.pct_black, c90s.geom FROM census_1990 AS c90 JOIN census_1990_shp AS c90s ON c90.gisjoin = c90s.gisjoin) AS c 
JOIN redline_poly on ST_Intersects(c.geom, redline_poly.geom) 
GROUP BY redline_poly.poly_id;



SELECT a.pct_black - avg(b.pct_black) AS avg_diff, a.poly_id, a.geom, a.holc_grade, b.holc_grade
FROM Census_Black_1990 a Census_Black_1990 b
WHERE a.holc_grade != b.holc_grade AND ST_Touches(a.geom, b.geom)



SELECT redline_poly.poly_id, avg(c.pct_black) AS pct_black, redline_poly.holc_grade_b, redline_poly.geom 
FROM (SELECT c90.pct_black, c90s.geom FROM census_1990 AS c90 JOIN census_1990_shp AS c90s ON c90.gisjoin = c90s.gisjoin) AS c 
JOIN redline_poly on ST_Intersects(c.geom, redline_poly.geom) 
GROUP BY redline_poly.poly_id;

#Weighted averages:
#https://gis.stackexchange.com/questions/40808/area-weighted-calculation-on-an-intersection

#Differences between cross-borders


