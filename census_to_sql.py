def census_to_sql(year):
	'''
	takes year as a parameter and returns SQL queries to create table in po
	'''
	table_name = census_ + str(year)
	create_table_str =  "CREATE TABLE " + table_name + " (geo_id varchar(50), geo_name varchar(50), ind_id varchar(10), life_exp float8, year int);"

	copy_str = " COPY " + table_name + "(geo_id, geo_name, ind_id, life_exp, year)"
	from_str = " FROM " + "'/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/census_" + year + ".csv' WITH CSV HEADER;"

return create_table_str + copy_str + from_str

s = postgres.connect()
c = s.cursor()

year_list = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
for year in year_list:
	query = census_to_sql(year)
	c.execute(query)