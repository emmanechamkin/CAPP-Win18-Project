# Create 1/4 mile buffers on either side of redline and join with census data

#Create table for borders
CREATE TABLE redline_borders
(a_gid int, b_gid int, a_grade varchar(80), b_grade varchar(80), geom geometry(LINESTRING), geom_buf_1 geometry, geom_buf_2 geometry);

#identify line segments where the polygons border and HOLC grades are different
INSERT INTO redline_borders (a_gid, b_gid, a_grade, b_grade, geom)
SELECT a.gid AS a_gid, b.gid AS b_gid, a.holc_grade AS a_grade, b.holc_grade AS b_grade, ST_Multi(ST_Intersection(a.geom,b.geom)) AS geom 
FROM redline a, redline b
WHERE a.gid < b.gid AND ST_Touches(a.geom, b.geom) AND a.holc_grade != b.holc_grade;

# use st dump to create lines
INSERT INTO redline_borders (a_gid, b_gid, a_grade, b_grade, geom)
SELECT a.gid AS a_gid, b.gid AS b_gid, a.holc_grade AS a_grade, b.holc_grade AS b_grade, (ST_Dump(ST_Intersection(a.geom,b.geom))).geom AS geom 
FROM redline a, redline b
WHERE a.gid < b.gid AND ST_Touches(a.geom, b.geom) AND a.holc_grade != b.holc_grade;


'''
capp30122=# INSERT INTO redline_borders (a_gid, b_gid, a_grade, b_grade, geom)
capp30122-# SELECT a.gid AS a_gid, b.gid AS b_gid, a.holc_grade AS a_grade, b.holc_grade AS b_grade, (ST_Dump(ST_Intersection(a.geom,b.geom))).geom AS geom 
capp30122-# FROM redline a, redline b
capp30122-# WHERE a.gid < b.gid AND ST_Touches(a.geom, b.geom) AND a.holc_grade != b.holc_grade;
ERROR:  Geometry type (LineString) does not match column type (MultiPoint)
capp30122=# drop table redline_borders;
DROP TABLE
capp30122=# CREATE TABLE redline_borders
capp30122-# (a_gid int, b_gid int, a_grade varchar(80), b_grade varchar(80), geom geometry(LINESTRING), geom_buf_1 geometry, geom_buf_2 geometry);
CREATE TABLE
capp30122=# INSERT INTO redline_borders (a_gid, b_gid, a_grade, b_grade, geom)
capp30122-# SELECT a.gid AS a_gid, b.gid AS b_gid, a.holc_grade AS a_grade, b.holc_grade AS b_grade, (ST_Dump(ST_Intersection(a.geom,b.geom))).geom AS geom 
capp30122-# FROM redline a, redline b
capp30122-# WHERE a.gid < b.gid AND ST_Touches(a.geom, b.geom) AND a.holc_grade != b.holc_grade;
ERROR:  Geometry type (Point) does not match column type (LineString)
'''

#Generate buffer around line segments and split into polygons
INSERT INTO redline_borders (geom_buf_1)
SELECT ST_AsText(geom)
FROM ST_Dump ((
SELECT 
ST_Polygonize(ST_Union(ST_Boundary(ST_Buffer(the_geom, 0.005, 'endcap=flat join=round')), the_geom)) AS buffer_sides 
FROM
  (SELECT ST_GeomFromEWKB(geom) AS the_geom FROM redline_borders) AS table1
));

UPDATE redline_borders SET geom=ST_MakeValid(geom_buf_1);

#https://postgis.net/docs/ST_Intersection.html


INSERT INTO redline_borders (geom_buf_2)
SELECT ST_OffsetCurve(geom, .005, 'join=mitre mitre_limit=5.0')
FROM redline_borders;

#https://trac.osgeo.org/postgis/wiki/UsersWikiSplitPolygonWithLineString

other option- use st.offset_curve
https://postgis.net/docs/ST_OffsetCurve.html 

'''
alternate plan:
1) identify all portions of polygons that touch where holc grades are different

SELECT a.gid AS gid_a, b.gid AS gid_b,
ST_Length(ST_CollectionExtract(ST_Intersection(a.geom, b.geom), 2))
FROM mypoly a, mypoly b
WHERE a.gid < b.gid AND ST_Touches(a.geom, b.geom) AND a.HOLC_grade != b.HOLC_grade;


https://stackoverflow.com/questions/31858612/calculate-length-of-a-shared-edge-of-two-polygones-in-postgis

2) create boundaries around each line segment

https://gis.stackexchange.com/questions/1197/creating-one-sided-buffers-or-parallel-lines-in-postgis

3) save to table?


step 1: create borders from multipolygons

SELECT gid, ST_Boundary(geom)::geometry(MULTILINESTRING,4326) As geom
    INTO line_layer
    FROM poly_layer;

https://gis.stackexchange.com/questions/163994/how-to-convert-multipolygon-to-multilinestring

step 1a: create new table with lines and include attribute of holc grades

step 2: figure out line segments that touch where holc grade is different

SELECT (b."GEM_NR")
FROM gemstat_simple5 as a
JOIN gemstat_simple5 as b
ON ST_Touches((a.the_geom),b.the_geom)
where a.spread =1;

Update gemstat_simple5 gem set spread=1, time=2
  FROM (
     SELECT (b."GEM_NR")
       FROM gemstat_simple5 as a,
            gemstat_simple5 as b
       WHERE ST_Touches(a.the_geom, b.the_geom) 
       AND a."GEM_NR" != b."GEM_NR"
       AND a.spread = 1
     ) as subquery
 WHERE gem."GEM_NR" = subquery."GEM_NR"

SELECT a.*
FROM polygon1 as a
JOIN polygon1 as b
ON st_intersects((st_buffer(a.the_geom,0.00001)),b.the_geom) 
where b.id = 561334;

Get boundary of multipolygon:

