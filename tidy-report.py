
# get-list-active-reports.py
from reportmanagementAPI import api_list_active_reports
from authenticationSupport import get_auth_structure, return_auth_token_from_auth_struct,renew_auth_structure
from reportmanagementAPI import  api_deactivate_report
#import utility
from utility import return_unique_report_name_stem
from json import dumps
import getopt
import sys
from json import loads
from reportmanagementSupport import get_list_int_active_reports
from re import search as research
auth_struct = get_auth_structure()
auth_token = return_auth_token_from_auth_struct(auth_struct)
 
def usage():
    print(sys.argv[0],"[-h|--help] [-j] reportNumber [reportNumber]")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hja:", ["help", "fileIDs=", "json","limit-reportIDs"]) 
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    # store report
# set up defaults
verbose=False
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
              accountIDs = acct_id_list
    else:
        assert False, "unhandled option"

num_array=[int(i) for i in args ]
if num_array == []:
	num_array = None

list = api_list_active_reports(auth_token,accountIDs=accountIDs).content.decode()
list_dict = loads(list)

from local_shelve_dbs import ix_reportid_db_to_dict
db_dict = ix_reportid_db_to_dict()
reports_array = [ db_dict[item][report]['reportID'] for item in db_dict for report in db_dict[item] ]
match_str = return_unique_report_name_stem()
for item in list_dict:
	if research(match_str,item['title']):
		reportID = item['reportID']
		reportID_str = str(reportID)
		#print("type: ",type(reportID)," value: ",reportID)
		reportID_int=int(reportID)
		if reportID_int in reports_array:
			print("skipping ",reportID_str," as in reportID db")
		else:
			auth_struct = renew_auth_structure(auth_struct)
			auth_token = return_auth_token_from_auth_struct(auth_struct)
			response = api_deactivate_report(auth_token,reportID_str)
			if response.status_code != 200:
				print("response for report id, ", reportID_str, ",is ",response.status_code)
			print("delete ",item['reportID'],":",item['title'])
	else:
		pass
		#print("Non match: ",item['title'])

def do_int():
	list_int = get_list_int_active_reports(auth_token)
	#list_int = [ item["fileID"] for item in list_json]
	if num_array != []:
		# limit if command line list
		list_set = set(list_int)
		list_set = list_set.intersection(set(num_array))
		list_int = [ int(id) for id in list_set ]

