File: README.txt
Contains: Instructions for how to run software on UChicago VMs

Installs required:
1. django (COMMAND: sudo pip3 install django)
2. leaflet (COMMAND: sudo pip3 install leaflet)
3. django-leaflet (COMMAND: sudo pip3 install django-leaflet)
4. psycopg2 (COMMAND: sudo pip3 install psycopg2)
5. postgres (COMMAND: sudo pip3 install postgres)
6. postgis  (COMMAND: sudo pip3 install postgis)

Clone the repository:
Navigating to the desired location and running the command 'git clone https://github.com/emmanechamkin/CAPP-Win18-Project/'

Steps to run the website:
1. Navigate to ~/CAPP-Win18-Project/Website/mysite in a terminal
2. Run the command 'python3 manage.py runserver'
3. In a browser, navigate to the location of the development server as stated in the terminal and add /home/, 
   this will likely be http://127.0.0.1:8000/home
4. Peruse the website at your leisure
5. To use the interactive map, use the left-hand sidebar to navigate to Maps (http://127.0.0.1:8000/home/maps),
   then choose variable and year of interest, toggle the border as desired and click "Submit" to render them map


Steps to duplicate the database:

1) Download postgres and postgis (I used Homebrew for my installation, see above for VM commands)

2) Create a postgis enabled postgres database using the following commands:

$ psql postgres; # from terminal
postgres=# CREATE DATABASE [database_name]; #in psql, replace [database_name] with your name
postgres=# \connect [database_name]
[database_name]=# CREATE EXTENSION postgis;
[database_name]=# 
INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 102003, 'esri', 102003, '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs ', 'PROJCS["USA_Contiguous_Albers_Equal_Area_Conic",GEOGCS["GCS_North_American_1983",DATUM["North_American_Datum_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["False_Easting",0],PARAMETER["False_Northing",0],PARAMETER["longitude_of_center",-96],PARAMETER["Standard_Parallel_1",29.5],PARAMETER["Standard_Parallel_2",45.5],PARAMETER["latitude_of_center",37.5],UNIT["Meter",1],AUTHORITY["EPSG","102003"]]');

The coordinate projection system for the ipums data is not native to postgis and therefore needs to be added manually to the spatial reference system table in postgis. I used the command above which I copied  directly from the following source:
https://wiki.pop.umn.edu:4443/index.php/More_Advanced_PostGIS_playing

Note that the formatting in the spatial reference system is very tempermental so I would recommend copying and pasting the insert query from the above. 

Note the database name, user name, password (should be '' unless you set the password), host, and port - we'll need these to create the database.

The creation of the Postgres database and all of our analysis can be replicated by running the following files (located in the analysis folder on github):

	1) census_to_pgsql.py
	2) redline_boundaries.py
	3) norm_median.py
	4) census_weighted_average.py
	5) data_cleaning_weighted_avg.py


3) Before running any of the files, update the included global variables at the top of each file as follows:
	FILE_PATH: file path of directory containing the data_for_db folder on the flash drive (in data_for_db folder)
	DB_NAME: name of postgresql database created above
	DB_USER: user name for postgresql database created above
	DB_PASS: password for postgresql database created above
	DB_HOST: host for postgresql database created above
	DB_PORT: port for postgresql database created above

Updating these variables will ensure that the functions can access the data_for_db data and successfully populate the local posgres database you have created.

Once the global variables in each file have been updated, you can replicate our analysis by running the files from the command line in the following order:

4) census_to_pgsql.py.  

Reads census data for each year into census_[year] postgres table and creates normalized median variable for each table

5) redline_boundaries.py

Reads University of Richmond HOLC boundaries shapfile into postgres and performs analysis to create redline_poly table of boundary buffer polygons in postgres database

6) norm_median.py

Calculates normalized median column for census year tables

7) census_weighted_avg.py

Performs analysis to identify overlap between boundary buffers and census units that meet or exceed defined thresholds, calculate weighted averages of census statistics for each boundary buffer. 

8) data_cleaning_weighted_avg.py

Performs final data cleaning and produces the census_weighted_avg.geojson file that is read into Django

We have also included a folder on the flash drive called "database tables" that represents an export of all of the processed tables (census_[year] for each year, redline_poly, and census_weighted_avg_all) in our database. 

