
#figure out different working directories

# import HOLC redline into postgres
shp2pgsql -s 4326 HOLC_chicago.shp public.redline | psql -d capp30122

#import CHA places data
ogr2ogr -f PostgreSQL \
PG:"host='localhost' user='alenastern' port='5432' \
dbname='capp30122' password=''" \
CHA_places.json 

#life expectancy by neighborhood
ogr2ogr -f GeoJSON -t_srs EPSG:4326 le_2010.geojson \
PG:"host='localhost' dbname='capp30122' user='alenastern' password='' port='5432'" \
-sql "SELECT life_exp, wkb_geometry  \
FROM life_exp JOIN cha_places_test ON life_exp.geo_name = cha_places_test.name \
WHERE year = 2010;"



ogr2ogr -f "GeoJSON" "le_2000.geojson"\
"PG:host=localhost dbname=capp30122 user=alenastern password='' port=5432" \
-sql "SELECT life_exp, wkb_geometry  \
FROM life_exp JOIN cha_places_test ON life_exp.geo_name = cha_places_test.name \
WHERE year = 2000;"

ogr2ogr -f GeoJSON le_2000.geojson \
"PG:host=localhost dbname=capp30122 user=alenastern password='' port=5432" \
-sql "SELECT life_exp, wkb_geometry  \
FROM life_exp JOIN cha_places_test ON life_exp.geo_name = cha_places_test.name \
WHERE year = 2000;"

#Import census shapefiles

#import 1940 ipums census shapefile
shp2pgsql -s 102003:4326 US_tract_1940.shp public.census_1940_shp | psql -d capp30122

#import 1950 ipums census shapefile
shp2pgsql -s 102003:4326 US_tract_1950.shp public.census_1950_shp | psql -d capp30122

#import 1960 ipums census shapefile
shp2pgsql -s 102003:4326 US_tract_1960.shp public.census_1960_shp | psql -d capp30122

#import 1970 ipums census shapefile
shp2pgsql -s 102003:4326 US_tract_1970.shp public.census_1970_shp | psql -d capp30122

#import 1980 ipums census shapefile
shp2pgsql -s 102003:4326 US_tract_1980.shp public.census_1980_shp | psql -d capp30122

#import 1990 ipums census shapefile
shp2pgsql -s 102003:4326 IL_block_1990.shp public.census_1990_shp | psql -d capp30122

#import 2000 ipums census shapefile
shp2pgsql -s 102003:4326 IL_block_2000.shp public.census_2000_shp | psql -d capp30122

#import 2010 ipums census shapefile
shp2pgsql -s 102003:4326 IL_block_2010.shp public.census_2010_shp | psql -d capp30122


#test export redline polygon
ogr2ogr -f "GeoJSON" C:\Users\alenastern\Desktop\redline_poly_a.geojson  \
PG:"host='localhost' dbname='capp30122' user='alenastern' password='' port='5432'" \
-sql "SELECT * from redline_poly;" -t_srs EPSG:4326

# export test census_all
ogr2ogr -f "GeoJSON" census_all_1990.geojson  \
PG:"host='localhost' dbname='capp30122' user='alenastern' password='' port='5432'" \
-sql "SELECT * from census_avg_all;" -t_srs EPSG:4326

#geoJSON of percent black holc grade in 1990
ogr2ogr -f GeoJSON -t_srs EPSG:4326 pctblack_holc_1990.geojson \
PG:"host='localhost' dbname='capp30122' user='alenastern' password='' port='5432'" 
-sql 

C

SELECT 

#life expectancy by neighborhood
ogr2ogr -f GeoJSON -t_srs EPSG:4269 census_pct_black.geojson \
PG:"host='localhost' dbname='capp30122' user='alenastern' password='' port='5432'" \
-sql "SELECT c90.pct_black, c90s.geom \
FROM census_1990 AS c90 JOIN census_1990_shp AS c90s ON c90.gisjoin = c90s.gisjoin;"
