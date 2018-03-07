#data cleaning 

#basic check of validity of data by taking averages
select avg(total_pop), avg(pct_white), avg(pct_black), avg(pct_other), avg(total_units), avg(Median), avg(pct_occupied), avg(pct_vacant), avg(pct_own_occ), avg(pct_rent_occ) from census_weighted_avg_all; 
select min(total_pop), min(pct_white), min(pct_black), min(pct_other), min(total_units), min(Median), min(pct_occupied), min(pct_vacant), min(pct_own_occ), min(pct_rent_occ) from census_weighted_avg_all; 
select max(total_pop), max(pct_white), max(pct_black), max(pct_other), max(total_units), max(Median), max(pct_occupied), max(pct_vacant), max(pct_own_occ), max(pct_rent_occ) from census_weighted_avg_all; 

#noted that the average of pct_occupied = '-Infinity'
select pct_occupied from census_weighted_avg_all where pct_occupied < -1;
#Two rows had values = '-Infinity' replace with -1 (value for missing data)
UPDATE Census_Weighted_Avg_All SET pct_occupied = -1 WHERE pct_occupied = '-Infinity';

#noted that average of Median = NaN, because contained 'NaN' values that were not updated with
#update NULL in function
SELECT min(median) from census_weighted_avg_all where median != 'NaN';
# min is -1.65 so set norm_med null to -99
SELECT SUM(CASE WHEN Median  ='NaN' THEN 1 END) AS count_null FROM census_weighted_avg_all;
UPDATE Census_Weighted_Avg_All SET Median = -1 WHERE Median = 'NaN';
UPDATE Census_Weighted_Avg_All SET norm_med = -99 WHERE norm_med = 'NaN'; 

#check averages again
select avg(case when pct_occupied > -1 then pct_occupied  end) from census_weighted_avg_all;
select avg(case when median > -1 then median end) from census_weighted_avg_all;

#pct_occ = 0.950268781563176
#median = 190901.216970817

