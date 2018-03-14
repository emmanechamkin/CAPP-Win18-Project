import psycopg2 
import os

DB_NAME = "CAPP30122"
DB_USER = "alenastern"
DB_PASS = ''
DB_HOST = "localhost"
DB_PORT = "5432"

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
        (median - (Select avg(median) from census_{} where median != 'NaN'))/
        (select stddev(median) from census_{} where median != 'NaN') 
        as norm_med from census_{};'''.format(year, year, year)
    update_table = '''update census_{} set norm_med= intermed.norm_med from 
    intermed where census_{}.gisjoin = intermed.gisjoin;'''.format(year,year)


    return (add_col, insert_table, update_table)
    

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
c = conn.cursor()


year_list = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
for year in year_list:
    if year > 1951 and year < 1981:
        #for years where median not included, set norm_med to default missing value
        c.execute("ALTER TABLE census_{} add norm_med float8;".format(year))
        c.execute("UPDATE census_{} SET norm_med = -99;".format(year))
    else:
        #Create intermediate table for calculation, then join calculated
        #normalized median into census table
        c.execute("create table intermed (gisjoin varchar(50), norm_med float8);")
        add, insert, update = normalized_median(year)
        c.execute(add)
        c.execute(insert)
        c.execute(update)
        c.execute("drop table intermed;")

conn.commit()
c.close()
conn.close()

