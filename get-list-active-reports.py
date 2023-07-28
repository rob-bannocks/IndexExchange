# get-list-active-reports.py
from reportmanagementAPI import api_list_active_reports
from authenticationSupport import get_auth_structure, return_auth_token_from_auth_struct
from json import dumps
import getopt
import sys
from json import loads
auth_struct = get_auth_structure()
auth_token = return_auth_token_from_auth_struct(auth_struct)
from reportmanagementSupport import get_list_int_active_reports
 
debug = False

def usage():
    print(sys.argv[0],"[-h|--help] [-j] reportNumber [reportNumber]")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hDja:", ["help", "debug", "fileIDs=", "json","limit-reportIDs"]) 
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    # store report
# set up defaults
verbose=False
debug=False
predefined = None
accountIDs=None
json=False
# proccess options    
for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o == "-D":
        debug=True
    elif o == "-j":
        json = True
    elif o == "-a":
        acct_id_list = a
        if acct_id_list != None:
              array = acct_id_list.split(",")
              try:
                acct_id_list = [ int(i) for i in array ]
              except:
                print("non numeric publisher list supplued with -l option")
                quit(1)
              if debug == True:
                print(" -a has restricted the publishers list to :",acct_id_list)
              accountIDs = acct_id_list
    else:
        assert False, "unhandled option"

num_array=[int(i) for i in args ]
if num_array == []:
	num_array = None

if debug == True:
    print("========")
    print("num array ",num_array)

if json == True :
	list = api_list_active_reports(auth_token,accountIDs=accountIDs).content.decode()
	print(type(list))
	list_dict = loads(list)
	print(type(list_dict))
else:
	list_int = get_list_int_active_reports(auth_token)
	#list_int = [ item["fileID"] for item in list_json]
	if num_array != None:
		if debug == True:
			print("num array ",num_array)
		# limit if command line list
		list_set = set(list_int)
		list_set = list_set.intersection(set(num_array))
		list_int = [ int(id) for id in list_set ]

if debug == True:
	for ele in args:
		if int(ele) in list_int:
			print("found ",ele)
		else:
			print("not found ", ele)

if json == True :
	print("------")
	print(dumps(list_dict,indent=2))
	#print(list_json)
else:
	print(sorted(list_int))

if debug == True:
	print(num_array)
