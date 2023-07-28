# mysql_db.py fule
# contains functions to add and extract things from the database
#
#

#import MySQLdb
from settings import get_mysql_username, get_mysql_password, get_mysql_hostname, get_mysql_db_name
from mysql.connector import connect
#from mysql.connector import MYSQL
#  import escape_string
#from mysql.connector import escape_string(str_to_escape)


def get_mysql_connection(username=None,password=None,database=get_mysql_db_name(),hostname=get_mysql_hostname()):


	if username == None:
		username = get_mysql_username()
	
	if password == None:
		password = get_mysql_password()

	mydb = None
	try:
		mydb = connect(
			host= hostname,
			user = username,
			password = password,
			database = database,
			auth_plugin='mysql_native_password'
		)

	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
		return None
	else:
		sql = "SET time_zone = 'UTC'"
		local_cursor = mydb.cursor()
		local_cursor.execute(sql)
		mydb.commit()
	
		return mydb


def close_connection(connection):
	connection.close()

def columns_to_percents(columns):
	innerlen = len(columns)-2
	if innerlen < -1 :
		print("Error must include at least one column")
		quit(1)
	placeholder = "%s"
	if innerlen >= 0 :
		if innerlen > 0:
			placeholder += " ,%s" * innerlen
			#placeholder += " %s" * innerlen
		placeholder += ", %s"
		#placeholder += " %s"
	return placeholder
	
def csv_list_to_db_row(cursor,table,csv):
	"""
	This function takes a whole CSV array with the 
	headings as the top row, row 0, and inserts into
	the database connected to with the cursor.
	
	Because of the chosen strategy to assimilate date
	with late data this is no longer used.
	"""

	columns = csv[0]
	values_sql = [ tuple (csv[i]) for i in range(1,len(csv))]

	placeholder = columns_to_percents(columns)
	columns_sql = "( " + " , ".join(columns) + " )"

	sql = "INSERT INTO "+table +" " + columns_sql + " VALUES (" + placeholder + ")" 

	return cursor.executemany(sql, values_sql)

def insert_csv_list_to_db(cursor,table,csv):
	"""
	
	"""
	
	columns = csv[0]
	for row in range(1,len(csv)):
		insert_or_update_db_row_cursor(cursor,table,columns,csv[row])
	
def insert_or_update_db_row(con,table,columns,values):
	insert_or_update_db_row_no_commit(con,table,columns,values)
	con.commit()

def insert_or_update_db_row_no_commit(con,table,columns,values):
	"""
	
	"""

	cursor = con.cursor()

	insert_or_update_db_row_cursor(cursor,table,columns,values)

def insert_or_update_db_row_cursor(cursor,table,columns,values):
	"""
	
	"""
	values = [ str(val) for val in values]
	# Error checking
	placeholder = columns_to_percents(columns)
	columns_sql = "( " + " , ".join(columns) + " )"

	sql = "INSERT INTO "+table +" " + columns_sql + " VALUES (" + placeholder + ") ON DUPLICATE KEY UPDATE " + ", ".join( [ str(i) + "= %s " for i in columns ])

	# values
	values_sql = tuple ( values )
	values_sql += tuple ( values )
	
	cursor.execute(sql, values_sql)

def select_column_with_cursor(cursor,table_name,result_columns,where_column=None,value=None):
	sql = "SELECT "+ result_columns + " FROM "+table_name

	if where_column != None:
		sql = sql + " WHERE "+ where_column+" = '" + value + "'"

	sql = sql +";"

	result = cursor.execute(sql)
		
	data = cursor.fetchall()

	return data

def delete_row_with_cursor(cursor,table_name,where_column,value):
	sql = "DELETE FROM "+table_name+" WHERE "+where_column+" = '"+ value + "';"

	result = cursor.execute(sql)

	return result
