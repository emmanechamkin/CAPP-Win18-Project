import psycopg2 
import os 

DB_NAME = "test"
DB_USER = "alenastern"
DB_PASS = ''
DB_HOST = "localhost"
DB_PORT = "5432"

def census_weighted_average(year):
    '''
    Calculates weighted average statistics for redline buffer boundaries by
    identifying census units that intersect each redline buffer boundary (at the
    threshold of the intersection representing 15% of the area of a tract/ 50% 
    of the intersection of a block or representing 70% of the area of the 
    boundary buffer) and calculating the average weighted by census unit total 
    population for each variable in the census data table in the given year. 

    Inputs:
        year (int): year of census data

    Returns:
        query (str): query to calculated weighted average for a given year and
            insert into Census_Weighted_Avg_All table
        update (str): query to update the year column in the 
            Census_Weighted_Avg_All table to add the given year
    '''
    insert = '''INSERT INTO Census_Weighted_Avg_All (poly_id, holc_bound, holc_grade, year, Total_Pop, 
    PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC, norm_med, geom) '''
    select = '''SELECT redline_poly.poly_id, redline_poly.holc_bound, redline_poly.holc_grade_b, avg(c.year), 
    avg(c.Total_Pop) AS Total_Pop, (SUM(c.pct_white*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_white, 
    (SUM(c.pct_black*c.total_pop)/(SUM(c.total_pop) + 1)) AS PCT_BLACK, (SUM(c.pct_other*c.total_pop)/(SUM(c.total_pop) + 1)) as pct_other, 
    (SUM(c.total_units*c.total_pop)/(SUM(c.total_pop) + 1)) AS total_units, (SUM(c.median*c.total_pop)/(SUM(c.total_pop) + 1)) AS median, 
    (SUM(c.pct_occupied*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_occupied, (SUM(c.pct_vacant*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_vacant, 
    (SUM(c.pct_own_occ*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_own_occ, (SUM(c.pct_rent_occ*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_rent_occ, 
    (SUM(c.norm_med*c.total_pop)/(SUM(c.total_pop) + 1)) AS norm_med, redline_poly.geom '''
    fr = '''FROM redline_poly LEFT JOIN (SELECT c{}.year, c{}.total_pop, c{}.pct_white, c{}.pct_black, c{}.pct_other, 
    c{}.total_units, c{}.median, c{}.pct_occupied, c{}.pct_vacant, c{}.pct_own_occ, c{}.pct_rent_occ, c{}.norm_med, 
    c{}s.geom FROM census_{} AS c{} JOIN census_{}_shp AS c{}s ON c{}.gisjoin = c{}s.gisjoin) AS c '''.format(year, year, year, year, 
        year, year, year, year, year, year, year, year, year, year, year, year, year, year, year)
    if year < 1990:
        join = '''ON ST_Intersects(redline_poly.geom, c.geom) AND (ST_Area(ST_Intersection(c.geom, redline_poly.geom)) 
        >= 0.15*ST_Area(c.geom) OR ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 0.70*ST_Area(redline_poly.geom)) 
            GROUP BY redline_poly.poly_id;'''
    else:
        join = '''ON ST_Intersects(redline_poly.geom, c.geom) AND (ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 
        0.50*ST_Area(c.geom) OR ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 0.70*ST_Area(redline_poly.geom)) 
            GROUP BY redline_poly.poly_id;'''

    query = insert + select + fr + join
    update = "UPDATE Census_Weighted_Avg_All SET Year = {} WHERE Year IS NULL;".format(year)

    return (query, update)


    

conn = psycopg2.connect(database=DB_NAME , user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
c = conn.cursor()

create = '''CREATE TABLE Census_Weighted_Avg_All (poly_id int, holc_bound varchar(10), holc_grade varchar(10), 
    year int, Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, Median float8, 
    PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8, norm_med float8, geom geometry);'''
c.execute(create)



census_years = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
var_list = ["Total_Pop", "PCT_WHITE", "PCT_BLACK", "PCT_OTHER", "TOTAL_UNITS", "Median", 
"PCT_OCCUPIED", "PCT_VACANT", "PCT_OWN_OCC", "PCT_RENT_OCC"]

for year in census_years:
    query, update = census_weighted_average(year)
    c.execute(query)
    c.execute(update)

for var in var_list:
    update_null = "UPDATE Census_Weighted_Avg_All SET {} = -1 WHERE {} IS NULL;".format(var, var)
    c.execute(update_null)

add_id_unique = "ALTER TABLE Census_Weighted_Avg_All ADD COLUMN id_unique varchar(10);"
update_id_unique = "UPDATE Census_Weighted_Avg_All SET id_unique = concat(poly_id::text, year::text);"
c.execute(add_id_unique)
c.execute(update_id_unique)

conn.commit()
c.close()
conn.close()

