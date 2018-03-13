import psycopg2 
import os

FILE_PATH = "/Users/alenastern/Documents/Win2018/CAPP30122/raw_data/"
DB_NAME = "test"
DB_USER = "alenastern"
DB_PASS = "''"
DB_HOST = "localhost"
DB_PORT = "5432" 

def holc_buffer(grade):
	'''
	For a given HOLC grade, creates a query to identify the borders where a holc 
	area of the given grade touches a holc area of a different grade, and creates 
	boundary buffer polygon representing a 1/4 mile buffer out from the border of 
	the HOLC area of the given grade into the neighboring HOLC area of a 
	different grade.

	Inputs:
		grade (str): string representing HOLC grade

	Returns:
		query (str): string with query to 
	'''

  	query = '''INSERT INTO redline_poly (gid, holc_grade_b, holc_grade_a, geom) 
          SELECT b.gid, b.holc_grade as holc_a, a.holc_grade as holc_b, 
          geometry(ST_Intersection(ST_Buffer(CAST(a.geom AS geography), 402), 
          b.geom)) FROM redline a, redline b  
          WHERE a.holc_grade = '{}' AND b.holc_grade != '{}' AND 
          ST_Intersects(ST_Buffer(CAST(a.geom AS geography), 402), 
          b.geom);'''.format(grade, grade)

  	return query

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, 
	host=DB_HOST, port=DB_PORT)
c = conn.cursor()

#Import redline boundaries shapefile
shp_read = "shp2pgsql -s 4326 {}HOLC_chicago.shp public.redline | psql -d {}".format(FILE_PATH, DB_NAME)
os.system(shp_read) 


holc_grade_list = ['A', 'B', 'C', 'D']

#create table for redline boundary buffer polygons
table = '''CREATE TABLE redline_poly (poly_id SERIAL PRIMARY KEY, gid int, 
	holc_grade_b varchar(10), holc_grade_a varchar(10), geom geometry);'''

c.execute(table)

#create buffers for each holc grade type
for grade in holc_grade_list:
  insert = holc_buffer(grade)
  c.execute(insert)

# Add column noting the border grades noted 'own grade - neighbor grade'
add_holc_bound = "ALTER TABLE redline_poly ADD COLUMN holc_bound varchar(10);"
update_holc_bound = '''UPDATE redline_poly SET holc_bound= concat(holc_grade_b, 
	'-', holc_grade_a);'''
c.execute(add_holc_bound)
c.execute(update_holc_bound)

conn.commit()
c.close()
conn.close()



