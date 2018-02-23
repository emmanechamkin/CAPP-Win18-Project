
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
WHERE year = 2010"