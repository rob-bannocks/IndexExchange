# cal_authenticationSupport_API.py

from cal_settings import cal_api_to_db_table_mapping_table_name,cal_api_key_table_name, cal_api_key_table_primary_key,cal_api_key_key_column
from mysql_db import get_mysql_connection, close_connection,insert_or_update_db_row_cursor,select_column_with_cursor

def get_auth_structure_from_publisher_id(id,cursor):
	key = get_api_key_from_db(id,cursor)

	# call to get auth key
	return key

def get_api_key_from_db(id,cursor):
	results = select_column_with_cursor(cursor,cal_api_key_table_name(),cal_api_key_key_column(),cal_api_key_table_primary_key(),id)
	if results == []:
		return None

	return results[0][0]

#cal_api_key_table_name, cal_api_key_table_primary_key
	
def add_api_key_to_db(publisher_id,apikey):
	data = [ "publisher_id","api_key"]
	data.append([publisher_id,apikey])
	return insert_or_update_db_row_cursor(cursor,auth_table,data)

def delete_api_key_from_db(cursor,publisher_id):
	auth_table = cal_api_key_table_name()
	where_column = cal_api_key_table_primary_key()
	# not yet implemented
	result =  delete_row_with_cursor(cursor,auth_table,where_column,value)


if "__main__" == __name__ :
	db = get_mysql_connection()
	if db == None:
		print("Error cannot connect to database")
		sysExit(1)

	cursor = db.cursor()

	id = str(191759)
	print("key:",get_auth_structure_from_publisher_id(id,cursor))
	print(get_api_key_from_db(id,cursor))
	
	db.close()
