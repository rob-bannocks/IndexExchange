# json-to-ix-reporti-db.py

# read the file from the command line
import getopt, sys

debug = False
def usage():
	print("args[0] json-filename")
try:
	opts, args = getopt.getopt(sys.argv[1:], "Dh", ["help", "output=","debug"])
except getopt.GetoptError as err:
	print(err)  # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
output = None
verbose = False
for o, a in opts:
	if o == "-D":
		debug == True
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	else:
		assert False, "unhandled option"

if len(args) != 1:
	print("Error this utility takes only one command line arguenment")
	sys.exit()

# just one file is dealtwith in this utlity
# get json as dict

from local_shelve_dbs import read_json_file_db
if debug == True:
	print("reaing file ",args[0])

dict = read_json_file_db(args[0])

from local_shelve_dbs import write_ix_reportid_db
write_ix_reportid_db(dict)
