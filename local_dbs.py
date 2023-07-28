# local_dbs.py

from mysql_db import select_column_with_cursor
from mysql_db import get_mysql_connection,close_connection

def return_publisherid_db():
	db = get_mysql_connection()	
	if db == None:
		print("Error cannot connect to db")

	cursor = db.cursor()

	data = select_column_with_cursor(cursor,"prog_ix_publishers","publisher_id,publisher,country")

	cursor.close()
	close_connection(db)

	if len(data ) == 0:
		return {}

	dict = { item[0] : item[1] for item in data }

	return dict
