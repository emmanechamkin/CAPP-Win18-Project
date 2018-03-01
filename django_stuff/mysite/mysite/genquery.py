import psycopg2 

### NOT A DJANGO FILE

DB = 'db'
TABLE = 'table'
GEOCODE = 'code'
GEOSHAPE = 'shape'

def connect(DB):
	try:
		conn = psycopg2.connect("dbname = 'name'")
	except:
		print ("i cannot connect to the database")

	cursor = conn.cursor()
	return cursor


def construct_query(args):
	yr = str(args['yr'])
	ind = args['ind']
	inc_str = ", ".join([ind, GEOCODE, GEOSHAPE])
	qstr = " ".join(["SELECT", inc_str, "FROM", TABLE, "WHERE year ==", yr])
	return qstr

def run_query(args):
	cursor = connect(DB)
	qstr = construct_query(args)
	cursor.execute(qstr)
	all_rows = cursor.fetchall()
	return all_rows 