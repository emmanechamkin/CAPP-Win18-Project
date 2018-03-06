import psycopg2 


def census_to_sql(year):
	'''
	takes year as a parameter and returns SQL queries to create table in po
	'''
	table_name = "census_" + str(year)
	create_table_str =  "CREATE TABLE " + table_name + " (GISJOIN varchar (50), YEAR int, BLOCKA varchar(10), BLOCK_GRPA int, TRACTA int, C_CITYA varchar(10), COUNTY varchar(20), MSA_CMSAA varchar(10), STATE varchar(10), Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));"
	copy_str = "COPY " + table_name + "(GISJOIN, year, BLOCKA, BLOCK_GRPA, TRACTA, C_CITYA, COUNTY, MSA_CMSAA, STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)"
	from_str = " FROM " + "'/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/census_files_" + str(year)+"/"+str(year)+"_census_data.csv' WITH DELIMITER AS '|' CSV HEADER NULL AS '';"

	return create_table_str,  copy_str + from_str

def old_census_to_sql(year):
	table_name = "census_" + str(year)
	if year <= 1951: 
		create_table_str =  "CREATE TABLE " + table_name + " (GISJOIN varchar (50), YEAR int, TRACTA int, COUNTY varchar(20), STATE varchar(10), Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));"
		copy_str = "COPY " + table_name + "(GISJOIN, year, TRACTA, COUNTY, STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)"	
	else:
		create_table_str =  "CREATE TABLE " + table_name + " (GISJOIN varchar (50), YEAR int, TRACTA int, COUNTY varchar(20), STATE varchar(10), Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));"
		copy_str = "COPY " + table_name + "(GISJOIN, year, TRACTA, COUNTY, STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)"	

	from_str = " FROM " + "'/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/Old census data/raw data 1940-1980/" + str(year)+"s census data raw/"+str(year)+"s_fordb.csv' WITH DELIMITER AS ',' CSV HEADER NULL AS '';"

	return create_table_str,  copy_str + from_str

'''
def census_to_sql_60_80(year):
	table_name = "census_" + str(year)
	create_table_str =  "CREATE TABLE " + table_name + " (GISJOIN varchar (50), YEAR int, TRACTA int, COUNTY varchar(20), STATE varchar(10), Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8, PRIMARY KEY (GISJOIN));"
	copy_str = "COPY " + table_name + "(GISJOIN, year, TRACTA, COUNTY, STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)"
	from_str = " FROM " + "'/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/Old census data/raw data 1940-1980/" + str(year)+"s census data raw/"+str(year)+"s_fordb.csv' WITH DELIMITER AS ',' CSV HEADER NULL AS '';"

	return create_table_str,  copy_str + from_str
'''


conn = psycopg2.connect(database="capp30122", user="alenastern", password='', host="localhost", port="5432")
c = conn.cursor()

year_list = [1990, 2000, 2010]
old_year_list = [1940, 1950, 1960, 1970, 1980]

for year in year_list:
	table, copy = census_to_sql(year)
	c.execute(table)
	c.execute(copy)


for year in old_year_list:
	table_old, copy_old = old_census_to_sql(year)
	c.execute(table_old)
	c.execute(copy_old)

ALTER TABLE census_1960 add Median float8;
UPDATE census_1960 SET Median = -1;

ALTER TABLE census_1970 add Median float8;
UPDATE census_1970 SET Median = -1;

ALTER TABLE census_1980 add Median float8;
UPDATE census_1980 SET Median = -1;


conn.commit()
c.close()
conn.close()
