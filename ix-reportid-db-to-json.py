# ix-reportid-db-to-json.py

from local_shelve_dbs import ix_reportid_db_to_dict
from json import dumps
import getopt
import sys

indent = 2
debug = False

def usage():
    print(sys.argv[0],"[-h|--help] [ -i indent ] [-d directory] [-D] publisherID [ publisherID ]")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hDi:", ["help", "debug", "indent ="]) 
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    # store report
# set up defaults
debug=False
# proccess options    
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o == "-D":
        debug=True
    elif o == "-i":
        indent = int(a)
    else:
        assert False, "unhandled option"

num_array=[int(i) for i in args ]
if num_array == []:
    num_array = None

dict = ix_reportid_db_to_dict()

if num_array != None:
	new_dict = {}
	for pub in num_array:
		new_dict[str(pub)] = dict[str(pub)]
	dict =new_dict
print(dumps(dict,indent=indent))
