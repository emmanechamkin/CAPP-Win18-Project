
import psycopg2

#load CHA life expectancy data
create_table_le = "create table life_exp (geo_id varchar(50), geo_name varchar(50), ind_id varchar(10), life_exp float8, year int, PRIMARY KEY (geo_name));"

copy_le = "COPY life_exp (geo_id, geo_name, ind_id, life_exp, year) FROM '/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/CHA_le.csv' WITH CSV HEADER;"

#load CHA overall health status data
create_table_ohs = "create table (geo_id varchar(50), geo_name varchar(50), ind_id varchar(10), ohs_hi_ci float8, ohs_low_ci float8, ohs_weight float8, wt_num float8, year int, PRIMARY KEY (geo_name));"

copy_ohs= "COPY overall_health (geo_id, geo_name, ind_id, ohs_hi_ci, ohs_low_ci, ohs_weight, wt_num, year) FROM '/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/ohs_2016.csv' WITH CSV HEADER;"

#load CHA infant mortality data
create_table_im = "create table infant_mortality (geo_id varchar(50), geo_name varchar(50), ind_id varchar(10), inf_mort_avg float8, inf_mort_crude float8, year int, PRIMARY KEY (geo_name));"

copy_im = "COPY infant_mortality(geo_id, geo_name, ind_id, inf_mort_avg, inf_mort_crude, year) FROM '/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/CHA_im.csv' WITH CSV HEADER;"


conn = psycopg2.connect(database="capp30122", user="alenastern", password='', host="localhost", port="5432")
c = conn.cursor()

c.execute(create_table_le)
c.execute(copy_le)
c.execute(create_table_ohs)
c.execute(copy_ohs)
c.execute(create_table_im)
c.execute(copy_im)

conn.commit()
c.close()
conn.close()