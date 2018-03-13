File: README.txt
Contains: Instructions for how to run software on UChicago VMs

Installs required:
1. django (COMMAND: sudo pip3 install django)
2. leaflet (COMMAND: sudo pip3 install leaflet)
3. django-leaflet (COMMAND: sudo pip3 install django-leaflet)
4. psycopg2 (COMMAND: sudo pip3 install psycopg2)
5. postgres (COMMAND: sudo pip3 install postgres)
6. postgis  (COMMAND: sudo pip3 install postgis)


Steps to duplicate the database:

1) Download postgres and postgis (I used Homebrew for my installation, see above for VM commands)

2) Create a postgis enabled postgres database using the following commands:

$ psql postgres; # from terminal
postgres=# CREATE DATABASE [database_name]; #in psql, replace [database_name] with your name
postgres=# \connect [database_name]
[database_name]=# CREATE EXTENSION postgis;

Note the database name, user name, password (should be '' unless you set the password), host, and port - we'll need these to create the database.

The creation of the Postgres database and all of our analysis can be replicated by running the following files (located in the analysis folder on github):

	1) census_to_pgsql.py
	2) redline_boundaries.py
	3) census_weighted_avg.py


3) Before running any of the files, update the global variables at the top of each file as follows:
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

6) census_weighted_avg.py

Performs analysis to identify overlap between boundary buffers and census units that meet or exceed defined thresholds, calculate weighted averages of census statistics for each boundary buffer, and perform final data cleaning. The function produces the census_all_final.geojson file that is read into Django

We have also included a folder on the flash drive called "database tables" that represents an export of all of the processed tables (census_[year] for each year, redline_poly, and census_weighted_avg_all) in our database. 

Steps to run the website:
1. Clone the reppository by navigating to the desired location and running the command 'git clone https://github.com/emmanechamkin/CAPP-Win18-Project/'
2. Navigate to ~/CAPP-Win18-Project/Website/mysite in a terminal
3. Run the command 'python3 manage.py runserver'
4. In a browser, navigate to the location of the development server as stated in the terminal and add /home/, 
   this will likely be http://127.0.0.1:8000/home
5. Peruse the website at your leisure
6. To use the interactive map, use the left-hand sidebar to navigate to Maps (http://127.0.0.1:8000/home/maps),
   then choose variable and year of interest, toggle the border as desired and click "Submit" to render them map
