import psycopg2 
import os

FILE_PATH = "/Users/alenastern/Documents/Win2018/CAPP30122/raw_data/"
DB_NAME = "test"
DB_USER = "alenastern"
DB_PASS = ''
DB_HOST = "localhost"
DB_PORT = "5432"

def census_to_sql(year):
	'''
	Imports census data from years after 1990 in csv to table in sql database.

	Inputs:
		year (int): year of census data
		file_path (str): file path where census data stored 

	Returns:
		create_table_str (str): string containing quary to create table in sql 
			database
		copy_str + from_str (str): string containing query to copy data from
			census csv file into sql table
	'''
	table_name = "census_" + str(year)
	create_table_str =  "CREATE TABLE " + table_name + ''' (GISJOIN varchar (50), 
	YEAR int, BLOCKA varchar(10), BLOCK_GRPA int, TRACTA int, C_CITYA varchar(10),
	COUNTY varchar(20), MSA_CMSAA varchar(10), STATE varchar(10), Total_Pop float8, 
	PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, 
	Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, 
	PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));'''
	copy_str = "COPY " + table_name + '''(GISJOIN, year, BLOCKA, BLOCK_GRPA, 
	TRACTA, C_CITYA, COUNTY, MSA_CMSAA, STATE, Total_Pop, PCT_WHITE, PCT_BLACK, 
	PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, 
	PCT_RENT_OCC)'''
	from_str = " FROM " + "'"FILE_PATH + str(year) +
	"_census_data.csv'WITH DELIMITER AS '|' CSV HEADER NULL AS '';"

	return create_table_str,  copy_str + from_str

def old_census_to_sql(year):
	'''
	Imports census data from years before 1990 in csv to table in sql database.

	Inputs:
		year (int): year of census data
		file_path (str): file path where census data stored 

	Returns:
		create_table_str (str): string containing quary to create table in sql 
			database
		copy_str + from_str (str): string containing query to copy data from
			census csv file into sql table
	'''
	table_name = "census_" + str(year)
	if year <= 1951: 
		create_table_str =  "CREATE TABLE " + table_name + ''' (GISJOIN varchar (50), 
		YEAR int, TRACTA int, COUNTY varchar(20), STATE varchar(10), 
		Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, 
		TOTAL_UNITS float8, Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, 
		PCT_OWN_OCC float8, PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));'''
		copy_str = "COPY " + table_name + '''(GISJOIN, year, TRACTA, COUNTY, 
		STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, 
		PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)'''	
	else:
		create_table_str =  "CREATE TABLE " + table_name + ''' (GISJOIN varchar (50), 
		YEAR int, TRACTA int, COUNTY varchar(20), STATE varchar(10), Total_Pop float8, 
		PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, 
		PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC 
		float8, PRIMARY KEY (GISJOIN));'''
		copy_str = "COPY " + table_name + '''(GISJOIN, year, TRACTA, COUNTY, STATE, 
		Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, PCT_OCCUPIED, 
		PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)'''	

	from_str = " FROM " + "'" +FILE_PATH+str(year)+
	"_census_data.csv' WITH DELIMITER AS ',' CSV HEADER NULL AS '';"

	return create_table_str,  copy_str + from_str

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
c = conn.cursor()

year_list = [1990, 2000, 2010]
old_year_list = [1940, 1950, 1960, 1970, 1980]

for year in year_list:
	table, copy = census_to_sql(year)
	c.execute(table)
	c.execute(copy)
	shp_read = "shp2pgsql -s 102003:4326 {}IL_block_{}.shp public.census_{}_shp | psql -d {}".format(FILE_PATH, year, year, DB_NAME)
	c.execute(shp_read)

for year in old_year_list:
	table_old, copy_old = old_census_to_sql(year)
	c.execute(table_old)
	c.execute(copy_old)
	shp_read = "shp2pgsql -s 102003:4326 {}US_tract_{}.shp public.census_{}_shp | psql -d {}".format(FILE_PATH, year, year, DB_NAME)
	os.system(shp_read)

c.execute("ALTER TABLE census_1960 add Median float8;")
c.execute("UPDATE census_1960 SET Median = 'NaN';")

c.execute("ALTER TABLE census_1970 add Median float8;")
c.execute("UPDATE census_1970 SET Median = 'NaN';")

c.execute("ALTER TABLE census_1980 add Median float8;")
c.execute("UPDATE census_1980 SET Median = 'NaN';")


conn.commit()
c.close()
conn.close()
