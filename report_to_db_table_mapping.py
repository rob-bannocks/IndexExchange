# report_to_table_mapping.py
#
# This file contains the report name to MySQL mapping table.
# NB this is a pyhon file and ensure any edits respect python syntax.
report_2_db_table_mapping = {
	'Generic Revenue Report' : { 'db_table': "prog_ix_stats"},
	'Generic Revenue Report Back dates' : { 'db_table' : "prog_ix_stats"},
	'Generic Revenue Report Last 7 days' : { 'db_table' : "prog_ix_stats"},
	'Generic Revenue Report for today only' : { 'db_table' : "prog_ix_stats", 'reportID' : 124},
}

if __name__ == "__main__":
	for item in report_2_db_table_mapping:
		print(item)
		dict=report_2_db_table_mapping[item]
		for key, value in dict.items():
			print("key = ",key," value = ",value)
