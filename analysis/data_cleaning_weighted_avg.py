import psycopg2
import os

DB_NAME = "CAPP30122"
DB_USER = "alenastern"
DB_PASS = ''
DB_HOST = "localhost"
DB_PORT = "5432"

#data cleaning 

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, 
	password=DB_PASS, host=DB_HOST, port=DB_PORT)
c = conn.cursor()

#basic check of validity of data by taking averages
c.execute('''select avg(total_pop), avg(pct_white), avg(pct_black), avg(pct_other), 
	avg(total_units), avg(Median), avg(pct_occupied), avg(pct_vacant), 
	avg(pct_own_occ), avg(pct_rent_occ) from census_weighted_avg_all;''') 
c.fetchone()
c.execute('''select min(total_pop), min(pct_white), min(pct_black), min(pct_other), 
	min(total_units), min(Median), min(pct_occupied), min(pct_vacant), 
	min(pct_own_occ), min(pct_rent_occ) from census_weighted_avg_all;''') 
c.fetchone()
c.execute('''select max(total_pop), max(pct_white), max(pct_black), max(pct_other), 
	max(total_units), max(Median), max(pct_occupied), max(pct_vacant), 
	max(pct_own_occ), max(pct_rent_occ) from census_weighted_avg_all;''') 
c.fetchone()
#noted that the average of pct_occupied = '-Infinity'
c.execute("select pct_occupied from census_weighted_avg_all where pct_occupied < -1;")
#Two rows had values = '-Infinity' replace with -1 (value for missing data)
c.execute("UPDATE Census_Weighted_Avg_All SET pct_occupied = -1 WHERE pct_occupied = '-Infinity';")

#noted that average of Median = NaN, because contained 'NaN' values that were not updated with
#update NULL in function
c.execute("SELECT min(median) from census_weighted_avg_all where median != 'NaN';")
# min is -1.65 so set norm_med null to -99
c.execute("SELECT SUM(CASE WHEN Median  ='NaN' THEN 1 END) AS count_null FROM census_weighted_avg_all;")
c.execute("UPDATE Census_Weighted_Avg_All SET Median = -1 WHERE Median = 'NaN';")
c.execute("UPDATE Census_Weighted_Avg_All SET norm_med = -99 WHERE norm_med = 'NaN';") 


conn.commit()
c.close()
conn.close()

#export cleaned data as geojson file for Django

export_gj = "ogr2ogr -f 'GeoJSON' census_weighted_avg.geojson PG:'host='{}' dbname='{}' user='{}' password='{}' port='{}'' -sql 'SELECT * from census_weighted_avg_all;' -t_srs EPSG:4326".format(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT)
os.system(export_gj)
