import psycopg2 

def holc_buffer(grade):
  query = "INSERT INTO redline_poly (gid, holc_grade_b, holc_grade_a, geom) \
          SELECT b.gid, b.holc_grade as holc_a, a.holc_grade as holc_b, \
          geometry(ST_Intersection(ST_Buffer(CAST(a.geom AS geography), 402), b.geom)) \
          FROM redline a, redline b  \
          WHERE a.holc_grade = '{}' AND b.holc_grade != '{}' AND \
          ST_Intersects(ST_Buffer(CAST(a.geom AS geography), 402), b.geom);".format(grade, grade)

  return query




conn = psycopg2.connect(database="capp30122", user="alenastern", password='', host="localhost", port="5432")
c = conn.cursor()

holc_grade_list = ['A', 'B', 'C', 'D']


table = "CREATE TABLE redline_poly (poly_id SERIAL PRIMARY KEY, gid int, holc_grade_b varchar(10), holc_grade_a varchar(10), geom geometry);"

c.execute(table)

for grade in holc_grade_list:
  insert = holc_buffer(grade)
  c.execute(insert)

add_holc_bound = "ALTER TABLE redline_poly ADD COLUMN holc_bound varchar(10);"
update_holc_bound = "UPDATE redline_poly SET holc_bound= concat(holc_grade_b, '-', holc_grade_a);"
c.execute(add_holc_bound)
c.execute(update_holc_bound)

conn.commit()
c.close()
conn.close()



