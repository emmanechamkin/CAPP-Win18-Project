import psycopg2 
import os 

FILE_PATH = "/Users/alenastern/Documents/Win2018/CAPP30122/raw_data/"
DB_NAME = "capp30122"
DB_USER = "alenastern"
DB_PASS = ''
DB_HOST = "localhost"
DB_PORT = "5432"

def census_to_sql(year, file_path = FILE_PATH):
	'''
	Imports census data in csv to table in sql database.

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
	#account for variations in fields across census years
	if year < 1951:
		median_create = " Median float8, "
		median_copy = " Median,"
		locality_create = " COUNTY varchar(20),"
		locality_copy = "COUNTY,"
		geography_create = ""
		geography_copy = ""
		delim = ","
	elif year < 1981:
		median_create = ""
		median_copy = ""
		locality_create = " COUNTY varchar(20),"
		locality_copy = "COUNTY,"
		geography_create = ""
		geography_copy = ""
		delim = ","
	else:
		median_create = " Median float8, "
		median_copy = " Median,"
		locality_create = ''' C_CITYA varchar(10), COUNTY varchar(20), 
			MSA_CMSAA varchar(10),'''
		locality_copy = "C_CITYA, COUNTY, MSA_CMSAA,"
		geography_create = "BLOCKA varchar(10), BLOCK_GRPA int,"
		geography_copy = "BLOCKA, BLOCK_GRPA,"
		delim = "|"


	create_table_str =  ("CREATE TABLE " + table_name +
	"(GISJOIN varchar (50), YEAR int, TRACTA varchar(10)," + geography_create + 
	locality_create +  ''' STATE varchar(10), Total_Pop float8, PCT_WHITE float8, 
	PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8,'''+ median_create 
	+ '''PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8,
	PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));''')
	copy_str = ("COPY " + table_name + "(GISJOIN, year, TRACTA, " + geography_copy +
	locality_copy + " STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS,"
	+ median_copy + " PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)")
	from_str = (" FROM " + FILE_PATH +str(year)+
	"_census_data.csv' WITH DELIMITER AS '{}' CSV HEADER NULL AS '';").format(delim)

	return create_table_str,  copy_str + from_str


def normalized_median(year):
    '''
	Performs calculations to generate normalized median variable for the census
	table in a given year. Normalized median is defined as follows:

		(median - mean(median))/std dev(median)

	Inputs:
		year (int): year of census data
	Returns:
		add_col (str): query to add column to census data table
		insert_table (str): query to insert gisjoin (unique ID) and standardized 
			median into intermediate table
		update_table (str): query to update census table for given year with
			standardized median data from intermediate table

	'''

    add_col = "ALTER TABLE census_{} add column norm_med float8;".format(year)
    insert_table = '''insert into intermed(gisjoin, norm_med) select gisjoin, 
        (median - (Select avg(median) from census_{} 
        where median != 'NaN'))/(select stddev(median) from census_{} 
        where median != 'NaN') as norm_med from census_{};'''.format(year, year, year)
    update_table = '''update census_{} set norm_med= intermed.norm_med from 
        intermed where census_{}.gisjoin = intermed.gisjoin;'''.format(year,year)


    return (add_col, insert_table, update_table)


conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, 
	host=DB_HOST, port=DB_PORT)
c = conn.cursor()
# The coordinate projection system used by IPUMS for shapefiles is not native
# to PostGIS so it must be added manually to the database spatial reference
# system. Code in execute statement below is directly copied from:
# https://wiki.pop.umn.edu:4443/index.php/More_Advanced_PostGIS_playing


year_list = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]

for year in year_list:
    # Create database table for census data for given year
    table, copy = census_to_sql(year)
    c.execute(table)
    c.execute(copy)
    # Import census geographic unit shapefile for given year
    if year > 1981:
        shp_name = FILE_PATH+"/IL_block_{}.shp".format(year)
    else:
        shp_name = FILE_PATH+"US_tract_{}.shp".format(year)
    table_name = "public.census_{}_shp".format(year)
    os.system("shp2pgsql -s 102003:4326 {} {} | psql -d {}".format(shp_name, table_name, DB_NAME))
    # Add Median column set to null value for years 1960, 1970, 1980 (where Median
    # not included in census data)
    if year > 1959 and year < 1981:
        c.execute("ALTER TABLE census_{} add Median float8;".format(year))
        c.execute("UPDATE census_{} SET Median = 'NaN';".format(year))

    # Add standardized median column to census table
    c.execute("create table intermed (gisjoin varchar(50), norm_med float8);")
    add, insert, update = normalized_median(year)
    c.execute(add)
    c.execute(insert)
    c.execute(update)
    c.execute("drop table intermed;")


conn.commit()
c.close()
conn.close()