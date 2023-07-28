#!python3
# delete-api-key.py

import getopt
from cal_settings import cal_api_key_table_name,cal_api_key_columns,cal_api_key_columns,select_column_with_cursor, cal_api_key_table_primary_key
from mysql_db import get_mysql_connection, close_connection,insert_or_update_db_row_cursor ,insert_csv_list_to_db, delete_row_with_cursor
import sys
debug = False

def usage():
	print(sys.argv[0]+" [-h] | publisher_id [ publisher_id ]")
try:
	opts, args = getopt.getopt(sys.argv[1:], "Dh")

except getopt.GetoptError as err:
	# print help information and exit:
	print(err)  # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
	output = None

for o, a in opts:
	if o == "-D":
		debug = True
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	else:
		assert False, "unhandled option"

auth_table = cal_api_key_table_name()
where_column = cal_api_key_table_primary_key()
db_conn = get_mysql_connection()
if db_conn == None:
	print("Error cannot connect to MySQL database")
	
cursor = db_conn.cursor()
if len(args) == 0:
	columns = ",".join(cal_api_key_columns() )
	data = select_column_with_cursor(cursor,auth_table,columns)
	if data == None or len(data) == 0:
		print("no data in table")
	else:
		for item in data:
			print(item[0],":",item[1])
else:
	# iterate args and delete from DB
	for value in args:
		if debug == True:
			print(id," : ",key)
		result =  delete_row_with_cursor(cursor,auth_table,where_column,value,debug=False)
		db_conn.commit()
	
	if debug == True:
		print(data)
cursor.close()
db_conn.close()
