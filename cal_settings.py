# cal_settings.py

from mysql_db import select_column_with_cursor,insert_or_update_db_row_cursor
from cal_utility import  url_to_fileid

def old():
	def cal_api_to_db_table_mapping(api_name):
		api_to_table = {
			"impression_events" : { "data" : "", download_log_table : "prog_ix_impressions_event_fileid" },
			"bid_events" :  { "data" : "", download_log_table : "prog_ix_bids_event_fileid" }
		}
			
		if api_name in api_to_table:
			return api_to_table[api_name]
		else:	
			return None

def cal_api_to_db_table_mapping_table_name():
	return "prog_ix_api_to_db_table_mapping"

def get_cal_data_table_by_api_with_cursor(cursor,api_name):
	sql_resp = get_cal_column_by_api_with_cursor(cursor,"data_table",api_name)

	if sql_resp == []:
		return None

	return sql_resp[0][0]

def get_cal_download_log_table_by_api_with_cursor(cursor,api_name):
	return get_cal_column_by_api_with_cursor(cursor,"download_log_table",api_name)[0][0]

def get_cal_column_by_api_with_cursor(cursor,result_column,api_name):
	data = select_column_with_cursor(cursor,cal_api_to_db_table_mapping_table_name(),result_column,"api",api_name)
	return data
	
def cal_db_get_row(table_name,column,value):

	db = get_mysql_connection()	
	if db == None:
		print("Error cannot connect to db")
	cursor = db.cursor()

	result = select_column_with_cursor(table_name,column,value)

	cursor.close()
	close_connection(db)

def return_apikey_table_with_cursor(cursor):
	#data = select_column_with_cursor(cursor,cal_api_key_table_name(),"*")
	columns = ",".join(return_apikey_table_columns_with_cursor(cursor))
	data = select_column_with_cursor(cursor,cal_api_key_table_name(),columns)
	return data

def cal_download_log_table_name():
	return "prog_ix_cal_download_log"

def return_download_log_table(cursor):
	download_log_sql = "SELECT * from "+cal_download_log_table_name()+";"
	result = cursor.execute(download_log_sql)
	return cursor.fetchall()

def return_download_log_table_as_publisher_id_list(cursor):
	result = return_download_log_table(cursor)
	if result == []:
		return result
	out = [ str(item[0]) for item in result ]
	return out


def RFC3339_to_mysql_datetime(hour):
	hour = hour.replace("T"," ")
	hour = hour.replace("Z","")
	return hour

def update_download_log_table_entry(cursor, hour, downloadURL, publisher_id, origin ):
	table_name = cal_download_log_table_name()
	
	fileid = url_to_fileid(downloadURL)
	try:
		fileid_int = int(fileid)
	except:
		print("[update_download_log_table_entry] called with invalid URL,",downloadURL)
		quit(1)

	columns = ["fileid","hour","downloadURL","publisher_id","origin"] # or ()

	hour = RFC3339_to_mysql_datetime(hour)
	values = [fileid,hour, downloadURL, publisher_id, origin] # or ()
	return_val = insert_or_update_db_row_cursor(cursor,table_name,columns,values)

	return return_val

def get_apikeys_table_name():
	return "prog_ix_apikeys"	

def return_table_definition_with_cursor(cursor,table_name):
	describe_sql = "DESCRIBE "+table_name
	result_c = cursor.execute(describe_sql)
	result = cursor.fetchall()
	return result

def return_table_feilds_with_cursor(cursor,table_name):

	result = return_table_definition_with_cursor(cursor,table_name)

	return [ str(item[0] ) for item in result ]

def return_int_feilds_from_table_definition(cursor,table_name, exclude_list=[]):

	result = return_table_definition_with_cursor(cursor,table_name)
	list = []
	for item in result:
		if item[1] == b'int':
			list.append(item[0])
	for item in exclude_list:
		if item in list:
			list.remove(item)
	return list

def return_apikey_table_columns_with_cursor(cursor):
	table_def = return_table_definition_with_cursor(cursor,get_apikeys_table_name())
	out = [ str(item[0]) for item in table_def ]
	return out

def cal_api_key_table_name():
	return "prog_ix_apikeys"

def cal_api_key_columns():
	return [ "publisher_id","api_key"]

def cal_api_key_table_primary_key():
	return cal_api_key_columns()[0]

def cal_api_key_key_column():
	return cal_api_key_columns()[1]
