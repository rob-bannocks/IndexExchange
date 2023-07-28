#!python3
# add-api-key.py

import getopt
from cal_settings import cal_api_key_table_name,cal_api_key_columns,cal_api_key_columns,select_column_with_cursor
from mysql_db import get_mysql_connection, close_connection,insert_or_update_db_row_cursor ,insert_csv_list_to_db
import sys
debug = False

def usage():
	print(sys.argv[0]+" [-h] | publisher_id hex-api-key [ publisher_id hex-api-key ]")
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

if len(args) % 2 == 1:
	print("Error odd number of arguenments need a number of publisher_id key pairs")
	usage()
	sys.exit(1)

auth_table = cal_api_key_table_name()
db_conn = get_mysql_connection()
if db_conn == None:
	print("Error cannot connect to MySQL database")
	
cursor = db_conn.cursor()
if len(args) == 0:
	columns = ",".join(cal_api_key_columns() )
	data = select_column_with_cursor(cursor,auth_table,columns,debug=debug)
	if data == None or len(data) == 0:
		print("no data in table")
	else:
		for item in data:
			print(item[0],":",item[1])
else:
	# transform arg pairs to dict
	evenargs=args[0::2]
	oddargs=args[1::2]
	if debug == True:
		print(evenargs)
		print(oddargs)
	
	out = [i for i in zip(evenargs,oddargs)]

	data = []
	data.append(cal_api_key_columns() )
	# iterate dict and add to db
	for id,key in out:
		if debug == True:
			print(id," : ",key)
		data.append([id,key])
	
	if debug == True:
		print(data)
	result = insert_csv_list_to_db(cursor,auth_table,data,debug=debug)
db_conn.commit()
cursor.close()
db_conn.close()
