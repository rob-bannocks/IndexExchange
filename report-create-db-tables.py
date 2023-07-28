# report-create-db-tables.py
#
# script to set up and initially populate the tables needed for the scripts to run


import mysql.connector
from mysql_db import insert_or_update_db_row_cursor,insert_csv_list_to_db
from mysql_db import get_mysql_connection, select_column_with_cursor
from settings import get_fileid_table_name,get_reportid_table_name
import sys
import getopt

do_fileid_table = True
do_reportid_table = True

def usage():
	print(sys.argv[0]+" [-h] | [ -D ] [ -f ] [ -r ] [ -F ] [ -R ]")
try:
	opts, args = getopt.getopt(sys.argv[1:], "DrfFR")
	if ( len(sys.argv) > 0 and "-D" not in opts )  or (  "-D" in opts and len(sys.argv)>1) :
		do_fileid_table = do_api_tables = do_api_tables_data = do_log_tables = do_mapping_tables = do_auth_table = False

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
	elif o in ("-F"):
		do_fileid_table = False
	elif o in ("-f"):
		do_fileid_table = True
	elif o in ("-r"):
		do_reportid_table = True
	elif o in ("-R"):
		do_reportid_table = False
	else:
		assert False, "unhandled option"
		print(do_mapping_tables )

if debug == True:
	print("do_fileid_tables ",do_fileid_table )
	print("do_reportid_tables ",do_reportid_table )

db_conn = get_mysql_connection()
if db_conn == None:
	print("Error cannot connect to MySQL database")

cursor = db_conn.cursor()

if do_fileid_table == True:
	fileid_table = get_fileid_table_name()
	fileid_sql = "create table "+fileid_table+" ( fileid int NOT NULL, publisher_id int NOT NULL, report_name varchar(255) NOT NULL, account_id int NOT NULL, status boolean NOT NULL default 0, file_status boolean NOT NULL default 0, db_status boolean NOT NULL default 0, reportid integer NOT NULL, PRIMARY KEY (fileid));"
	fileid_sql_grant = "grant select,update,insert on prog_stats."+ fileid_table + " to iximport@localhost ;"
	if debug == True:
		print("fileid_table:",fileid_table)
		print("fileid_sql:",fileid_sql)
		print("fileid_sql_grant:",fileid_sql_grant)
	cursor.execute(fileid_sql)
	db_conn.commit()

	cursor.execute(fileid_sql_grant)
	db_conn.commit()

if do_reportid_table == True:
	reportid_table = get_reportid_table_name()
	reportid_sql = "create table "+reportid_table+" ( account_id int NOT NULL, report_name varchar(255) NOT NULL, reportid int NOT NULL, created datetime NOT NULL, last_updated datetime, PRIMARY KEY(account_id,report_name));"
	reportid_sql_grant = "grant select,update,insert on prog_stats." + reportid_table + " to iximport@localhost ;"
	if debug == True:
		print("reportid_table:",reportid_table)
		print("reportid_sql:",reportid_sql)
		print("reportid_sql_grant:",reportid_sql_grant)

	cursor.execute(reportid_sql)
	db_conn.commit()
	cursor.execute(reportid_sql_grant)
	db_conn.commit()
	
#Closing the connection(s)
cursor.close()
db_conn.close()
