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
    #Create insert statement
    insert = '''INSERT INTO Census_Weighted_Avg_All (poly_id, holc_bound, 
        holc_grade, year, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, 
        TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, 
        PCT_RENT_OCC, norm_med, geom) '''
    # Create select statement to select weighted averages
    select = '''SELECT redline_poly.poly_id, redline_poly.holc_bound, 
        redline_poly.holc_grade_b, avg(c.year), avg(c.Total_Pop) AS Total_Pop, 
        (SUM(c.pct_white*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_white, 
        (SUM(c.pct_black*c.total_pop)/(SUM(c.total_pop) + 1)) AS PCT_BLACK, 
        (SUM(c.pct_other*c.total_pop)/(SUM(c.total_pop) + 1)) as pct_other, 
        (SUM(c.total_units*c.total_pop)/(SUM(c.total_pop) + 1)) AS total_units, 
        (SUM(c.median*c.total_pop)/(SUM(c.total_pop) + 1)) AS median, 
        (SUM(c.pct_occupied*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_occupied, 
        (SUM(c.pct_vacant*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_vacant, 
        (SUM(c.pct_own_occ*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_own_occ, 
        (SUM(c.pct_rent_occ*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_rent_occ, 
        (SUM(c.norm_med*c.total_pop)/(SUM(c.total_pop) + 1)) AS norm_med, 
        redline_poly.geom '''
    #create from statement 
    fr = '''FROM redline_poly LEFT JOIN (SELECT c{}.year, c{}.total_pop, 
        c{}.pct_white, c{}.pct_black, c{}.pct_other, c{}.total_units, 
        c{}.median, c{}.pct_occupied, c{}.pct_vacant, c{}.pct_own_occ, 
        c{}.pct_rent_occ, c{}.norm_med, c{}s.geom FROM census_{} AS c{} 
        JOIN census_{}_shp AS c{}s ON c{}.gisjoin = c{}s.gisjoin) AS c '''.format(year, 
        year, year, year, year, year, year, year, year, year, year, year, year, 
        year, year, year, year, year, year)

    #create join statement applying different overlap thresholds for bloc/tract years
    if year < 1990:
        join = '''ON ST_Intersects(redline_poly.geom, c.geom) AND 
            (ST_Area(ST_Intersection(c.geom, redline_poly.geom)) 
            >= 0.15*ST_Area(c.geom) OR ST_Area(ST_Intersection(c.geom, 
            redline_poly.geom)) >= 0.70*ST_Area(redline_poly.geom)) 
            GROUP BY redline_poly.poly_id;'''
    else:
        join = '''ON ST_Intersects(redline_poly.geom, c.geom) AND 
            (ST_Area(ST_Intersection(c.geom, redline_poly.geom)) 
            >= 0.50*ST_Area(c.geom) OR ST_Area(ST_Intersection(c.geom, 
            redline_poly.geom)) >= 0.70*ST_Area(redline_poly.geom)) 
            GROUP BY redline_poly.poly_id;'''

    query = insert + select + fr + join
    #create quety to add year column to data
    update = '''UPDATE Census_Weighted_Avg_All SET Year = {} 
            WHERE Year IS NULL;'''.format(year)

    return (query, update)

insert = "INSERT INTO Census_Weighted_Avg_All (poly_id, holc_bound, holc_grade, year, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC, norm_med, geom) "
    select = "SELECT redline_poly.poly_id, redline_poly.holc_bound, redline_poly.holc_grade_b, avg(c.year), avg(c.Total_Pop) AS Total_Pop, (SUM(c.pct_white*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_white, (SUM(c.pct_black*c.total_pop)/(SUM(c.total_pop) + 1)) AS PCT_BLACK, (SUM(c.pct_other*c.total_pop)/(SUM(c.total_pop) + 1)) as pct_other, \
            (SUM(c.total_units*c.total_pop)/(SUM(c.total_pop) + 1)) AS total_units, (SUM(c.median*c.total_pop)/(SUM(c.total_pop) + 1)) AS median, (SUM(c.pct_occupied*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_occupied, (SUM(c.pct_vacant*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_vacant, \
            (SUM(c.pct_own_occ*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_own_occ, (SUM(c.pct_rent_occ*c.total_pop)/(SUM(c.total_pop)+1)) AS pct_rent_occ, (SUM(c.norm_med*c.total_pop)/(SUM(c.total_pop) + 1)) AS norm_med, redline_poly.geom "
    fr = "FROM redline_poly LEFT JOIN (SELECT c{}.year, c{}.total_pop, c{}.pct_white, c{}.pct_black, c{}.pct_other, c{}.total_units, c{}.median, c{}.pct_occupied, c{}.pct_vacant, c{}.pct_own_occ, \
    c{}.pct_rent_occ, c{}.norm_med, c{}s.geom FROM census_{} AS c{} JOIN census_{}_shp AS c{}s ON c{}.gisjoin = c{}s.gisjoin) AS c ".format(year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year)
    if year < 1990:
        join = "ON ST_Intersects(redline_poly.geom, c.geom) AND (ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 0.15*ST_Area(c.geom) OR ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 0.70*ST_Area(redline_poly.geom)) \
            GROUP BY redline_poly.poly_id;"
    else:
        join = "ON ST_Intersects(redline_poly.geom, c.geom) AND (ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 0.50*ST_Area(c.geom) OR ST_Area(ST_Intersection(c.geom, redline_poly.geom)) >= 0.70*ST_Area(redline_poly.geom)) \
            GROUP BY redline_poly.poly_id;"

    query = insert + select + fr + join
    update = "UPDATE Census_Weighted_Avg_All SET Year = {} WHERE Year IS NULL;".format(year)



conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, 
    host=DB_HOST, port=DB_PORT)
c = conn.cursor()

# Create table to hold analyzed data in postgres 
create = '''CREATE TABLE Census_Weighted_Avg_All (poly_id int, 
    holc_bound varchar(10), holc_grade varchar(10), year int, 
    Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, 
    TOTAL_UNITS float8, Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, 
    PCT_OWN_OCC float8, PCT_RENT_OCC float8, norm_med float8, geom geometry);'''

c.execute(create)

# add census data to postgres for each year in census year list
census_years = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
var_list = ["Total_Pop", "PCT_WHITE", "PCT_BLACK", "PCT_OTHER", "TOTAL_UNITS", 
    "Median", "PCT_OCCUPIED", "PCT_VACANT", "PCT_OWN_OCC", "PCT_RENT_OCC"]

for year in census_years:
    query, update = census_weighted_average(year)
    c.execute(query)
    c.execute(update)

#for var in var_list:
#    update_null = '''UPDATE Census_Weighted_Avg_All SET {} = -1 WHERE {} 
#    IS NULL;'''.format(var, var)
#    c.execute(update_null)

add_id_unique = '''ALTER TABLE Census_Weighted_Avg_All ADD COLUMN 
    id_unique varchar(10);'''
update_id_unique = '''UPDATE Census_Weighted_Avg_All SET id_unique = 
    concat(poly_id::text, year::text);'''
c.execute(add_id_unique)
c.execute(update_id_unique)

#Data Cleaning 

#basic check of validity of data by taking averages
c.execute('''select avg(total_pop), avg(pct_white), avg(pct_black), 
    avg(pct_other), avg(total_units), avg(Median), avg(pct_occupied), 
    avg(pct_vacant), avg(pct_own_occ), 
    avg(pct_rent_occ) from census_weighted_avg_all;''')
c.fetchone() 
c.execute('''select min(total_pop), min(pct_white), min(pct_black), 
    min(pct_other), min(total_units), min(Median), min(pct_occupied), 
    min(pct_vacant), min(pct_own_occ), 
    min(pct_rent_occ) from census_weighted_avg_all;''')
c.fetchone() 
c.execute('''select max(total_pop), max(pct_white), max(pct_black), 
    max(pct_other), max(total_units), max(Median), max(pct_occupied), 
    max(pct_vacant), max(pct_own_occ), 
    max(pct_rent_occ) from census_weighted_avg_all;''')
c.fetchone() 

#noted that the average of pct_occupied = '-Infinity' 
#replace with -1 (value for missing data)
c.execute('''UPDATE Census_Weighted_Avg_All SET pct_occupied = -1 WHERE 
    pct_occupied = '-Infinity';''')

#noted that average of Median and Norm_Med= NaN, because contained 'NaN' values 
#that were not updated with update NULL in function
c.execute("SELECT min(median) from census_weighted_avg_all where median != 'NaN';")
c.fetchone()
# min is -1.65 so set norm_med null to -99
c.execute("UPDATE Census_Weighted_Avg_All SET Median = -1 WHERE Median = 'NaN';")
c.execute("UPDATE Census_Weighted_Avg_All SET norm_med = -99 WHERE norm_med = 'NaN';") 

conn.commit()
c.close()
conn.close()

gj_export = '''ogr2ogr -f "GeoJSON" census_all_final.geojson PG:"host='{}' dbname='{}' user='{}' password='{}' port='{}'" -sql "SELECT * from Census_Weighted_Avg_All;" -t_srs EPSG:4326'''.format(DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT)
os.system(gj_export)








