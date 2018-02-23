
# import HOLC redline into postgres
shp2pgsql -s 4326 HOLC_chicago.shp public.redline | psql -d capp30122

#import CHA places data
ogr2ogr -f PostgreSQL \
PG:"host='localhost' user='postgres' port='5432' \
dbname='capp30122' password=''" \
CHA_places.json 
