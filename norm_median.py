import psycopg2 

def normalized_median(year):
    add_col = "ALTER TABLE census_{} add column norm_med float8;".format(year)
    insert_table = "insert into intermed(gisjoin, norm_med) select gisjoin, (median - (Select avg(median) from census_{} where median != 'NaN'))/(select stddev(median) from census_{} where median != 'NaN') as norm_med from census_{};".format(year, year, year)
    update_table = "update census_{} set norm_med= intermed.norm_med from intermed where census_{}.gisjoin = intermed.gisjoin;".format(year,year)


    return (add_col, insert_table, update_table)
    



conn = psycopg2.connect(database="capp30122", user="alenastern", password='', host="localhost", port="5432")
c = conn.cursor()


year_list = [1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
for year in year_list:
    c.execute("create table intermed (gisjoin varchar(50), norm_med float8);")
    add, insert, update = normalized_median(year)
    c.execute(add)
    c.execute(insert)
    c.execute(update)
    c.execute("drop table intermed;")

conn.commit()
c.close()
conn.close()


'''
### final answer
create table intermed (gisjoin varchar(50), norm_med float8);


update census_1940 
set norm_med= intermed.norm_med
from intermed where census_1940.gisjoin = intermed.gisjoin;

insert into intermed(gisjoin, norm_med) select gisjoin, (median - (Select avg(median) from census_1950 where median != 'NaN'))/(select stddev(median) from census_1950 where median != 'NaN') as norm_med from census_1950;

update census_1950 
set norm_med= intermed.norm_med
from intermed where census_1950.gisjoin = intermed.gisjoin;
'''