# local_shelve_dbs.py

# 
from json import dumps
from json import load
from os.path import join
from os.path import exists
from shelve import open as shopen
from os.path import exists
from settings import get_index_exchange_settings_dir

def get_ix_reportid_db_filepath(dir = get_index_exchange_settings_dir()):
	"""

	"""
	filename = "ix_reportid_db.shelve"
	filepath = join(dir,filename)
	return filepath

def return_ix_reportid_db(filepath = get_ix_reportid_db_filepath()):
	try:
		d= shopen(filepath,"c")
	except:
		print("failed to ipen ix_reportIDs_db ",filepath)
		quit(1)
	return d

def read_shelve_file_db(filepath):
	dict={}
	with shopen(filepath,"c") as db:
		for key in list(db.keys()):
			dict[key] = db[key]
		db.close()
	return dict

def read_ix_reportid_db(filepath = get_ix_reportid_db_filepath()):
	return read_shelve_file_db(filepath)


def write_shelve_file_db(db_dict,filepath):
	#with open(filepath+".json","w") as f:
	#	f.write(dumps(db_dict,indent=1) )
	#	f.close()

	with shopen(filepath,"c") as db:
		for key in list(db_dict.keys()):
			db[key] = db_dict[key]
		db.close()
	
def ix_reportid_db_to_dict(filename = get_ix_reportid_db_filepath()):	
	dict = read_ix_reportid_db(filename)
	return dict

def ix_reportid_db_to_json(filename = get_ix_reportid_db_filepath(),indent = 1):	
	return dumps(ix_reportid_db_to_dict(filename),indent=indent)

def write_ix_reportid_db(ix_reportid_dict,filepath = get_ix_reportid_db_filepath()):
	return write_shelve_file_db(ix_reportid_dict,filepath)

def print_dict(dict):
	for item in dict:
		print(item)
		elem=dict[item]
		for key, value in elem.items():
			print("key = ",key," value = ",value)


def check_local_json_db_exists_or_create(filepath):
	if not exists(filepath):
		with open(filepath,"w") as f:
			f.write("{}")
			f.close()

def read_json_file_db(filepath):
	with open(filepath, "r") as f:
		db_dict = load(f)
	
	return db_dict

def write_json_file_db(db_dict,filepath):
	with open(filepath,"w") as f:
		f.write(dumps(db_dict,indent=1) )
		f.close()
if __name__ == "__main__":
	test = read_ix_reportid_db()
	test_file_shelve_db = "test-shelve-file-db.shelve"
	print(test)
	print(type(test))
	print("+===========+=======+=======+=====")
	dict = {
	"0" :{'Test Generic Revenue Report' : { 'reportID' : 8, 'db_table': "prog_ix_stats"},
		'Test Generic Revenue Report Back dates' : { 'reportID' : 68, 'db_table' : "prog_ix_stats"},
		'Test Generic Revenue Report Last 7 days' : { 'reportID' : 78, 'db_table' : "prog_ix_stats"},
		'Test Generic Revenue Report for today only' : { 'reportID' : 98, 'db_table' : "prog_ix_stats", 'reportID' : 124},
		}
	}
	
	#[ dict[pub][rep]['CreationDate'] = "date" for report in dict[pub] for pub in dict ]
	for item in dict:
		for item2 in dict[item]:
			dict[item][item2]['CreationDate']="Well this is good"
	print(dict)
	print_dict(dict)
	write_ix_reportid_db(dict)
	nd = read_ix_reportid_db()
	print(nd)
