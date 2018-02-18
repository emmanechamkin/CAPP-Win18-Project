#load CHA life expectancy data
create table life_exp
(geo_id varchar(50), geo_name varchar(50), ind_id varchar(10), 
life_exp float8, year int);

COPY life_exp (geo_id, geo_name, ind_id, life_exp, year)
FROM '/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/CHA_le.csv' WITH CSV HEADER;

#load CHA overall health status data
create table overall_health
(geo_id varchar(50), geo_name varchar(50), ind_id varchar(10), 
ohs_hi_ci float8, ohs_low_ci float8, ohs_weight float8, wt_num float8,
year int);

COPY overall_health (geo_id, geo_name, ind_id, ohs_hi_ci, ohs_low_ci, 
	ohs_weight, wt_num, year)
FROM '/Users/alenastern/Documents/Win2018/CAPP30122/CAPP-Win18-Project/data/ohs_2016.csv' WITH CSV HEADER;

#wriigig