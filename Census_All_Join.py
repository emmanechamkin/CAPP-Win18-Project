import psycopg2 

def census_average(year):

    insert = "INSERT INTO Census_Avg_All (poly_id, year, Total_Pop, PCT_WHITE, PCT_BLACK, PCT_OTHER, TOTAL_UNITS, Median, PCT_OCCUPIED, PCT_VACANT, PCT_OWN_OCC, PCT_RENT_OCC, geom) "
    select = "SELECT redline_poly.poly_id, avg(c.year), avg(c.Total_Pop) AS Total_Pop, avg(c.pct_white) AS pct_white, avg(c.pct_black) AS PCT_BLACK, avg(c.pct_other) as pct_other, \
            avg(c.total_units) AS total_units, avg(c.median) AS median, avg(c.pct_occupied) AS pct_occupied, avg(c.pct_vacant) AS pct_vacant, \
            avg(c.pct_own_occ) AS pct_own_occ, avg(c.pct_rent_occ) AS pct_rent_occ, redline_poly.geom "
    fr = "FROM (SELECT c{}.year, c{}.total_pop, c{}.pct_white, c{}.pct_black, c{}.pct_other, c{}.total_units, c{}.median, c{}.pct_occupied, c{}.pct_vacant, c{}.pct_own_occ, \
    c{}.pct_rent_occ, c{}s.geom FROM census_{} AS c{} JOIN census_{}_shp AS c{}s ON c{}.gisjoin = c{}s.gisjoin) AS c ".format(year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year) 
    join = "JOIN redline_poly on ST_Intersects(c.geom, redline_poly.geom) GROUP BY redline_poly.poly_id;"

    return insert + select + fr + join

conn = psycopg2.connect(database="capp30122", user="alenastern", password='', host="localhost", port="5432")
c = conn.cursor()

create = "CREATE TABLE Census_Avg_All (poly_id int, year int, Total_Pop float8, PCT_WHITE float8, PCT_BLACK float8, PCT_OTHER float8, TOTAL_UNITS float8, Median float8, PCT_OCCUPIED float8, PCT_VACANT float8, PCT_OWN_OCC float8, PCT_RENT_OCC float8, geom geometry);"
c.execute(create)

census_years = [1990]

for year in census_years:
    query = census_average(year)
    c.execute(query)

conn.commit()
c.close()
conn.close()
