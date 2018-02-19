def census_to_sql(year):
	'''
	takes year as a parameter and returns SQL queries to create table in po
	'''
	table_name = "census_" + str(year)
	create_table_str =  "CREATE TABLE " + table_name + " (GISJOIN varchar (50), YEAR int, BLOCKA varchar(10), BLOCK_GRPA int, TRACTA int, C_CITYA varchar(10), COUNTY varchar(10), MSA_CMSAA varchar(10), STATE varchar(10), Total_Pop int, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS int, Median int, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8);"
	copy_str = "COPY " + table_name + "(GISJOIN, year, BLOCKA, BLOCK_GRPA, TRACTA, C_CITYA, COUNTY, MSA_CMSAA, STATE, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC)"
	from_str = " FROM " + "'/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/census_files_" + str(year)+"/"+str(year)+"_census_data.csv' WITH DELIMITER AS '|' CSV HEADER;"

	return create_table_str,  copy_str + from_str


#s = postgres.connect()
#c = s.cursor()

#year_list = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2000]
#for year in year_list:
#	query = census_to_sql(year)
#	c.execute(query)