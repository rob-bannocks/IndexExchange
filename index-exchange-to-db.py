import json
from report_to_db_table_mapping import report_2_db_table_mapping
from getopt import getopt,GetoptError
from reportmanagementSupport import upload_existing_report, run_adhoc_report_to_download
from reportdownloadSupport import get_list_avaliable_fileIDs
from reportdownloadSupport import get_a_report_run_or_null
from csv import reader
from utility import text_to_csv
from utility import report_run_to_csv
from readwrite import write_list_to_csv_file
from indexExchangeToDBSupport import return_publishers_list
from indexExchangeToDBSupport import upload_and_run_reports_for_list
from indexExchangeToDBSupport import fetch_report_runs
from settings import get_templates_store
import sys
from authenticationSupport import return_auth_token_from_auth_struct,renew_auth_structure
from authenticationSupport import get_auth_structure

# First deal with the command line args and default settings


def usage():
    print(sys.argv[0],"[-h|--help] [ -n ] [-l publisherid [, publisherid] ] [-d directory] [-n] [-D] [ -R ] [ -r retries] Report-Name [Report-name]...")
# get report from command line
try:
    opts, args = getopt(sys.argv[1:], "hDd:nBr:sl:vR", ["help", "Debug" ,"outputDir=","copy-csv-files","copy-data-base","retries","silent-on-outcome-report","list-of-publishers-to-limit","verbose","Activity-report"])
except GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    # store report
# set up defaults
store_dir = get_templates_store()
verbose=False
use_report_number_for_filename=False
max_retries = 15
poduce_outcome_report = True
limit_list = None
activity_report=False
# proccess options    
write_to_database = True
write_to_file = False
# for testing
#write_to_database = False
#write_to_file = True
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-d" ):
        store_dir = a
    elif o == "-n":
        write_to_file = True
    elif o == "-B":
        write_to_database = False
    elif o == "-s":
        poduce_outcome_report = False
    elif o == "-r":
        max_retries = int(a)
    elif o == "-l":
        limit_list = a
    elif o == "-R":
        activity_report=True
    elif o == "-v":
        verbose = True
        print("verbose set on")
    else:
        assert False, "unhandled option"

#
# pyblishers.py should have a list of publushers in python dic format and assign to the
# variable publishers
#
# sanity check that each report requested on the command line is in the db table mapping file or stop
for report in args:
	if not report in report_2_db_table_mapping:
		print("No mapping for requested report,"+report+" in mapping file.  Cannot continue")
		quit(1)

list = return_publishers_list()
#
# sanity check. 
# must have at least one publisher
#

if len(list) == 0:
	print("Error no publishers in publishers file or no file.  Cannot continue")
	quit(1)

# process if -l command line arg
# This restricts the publishers processed to those supplied with the -l option
if limit_list != None:
	array = limit_list.split(",")
	try:
		cmd_list = [ int(i) for i in array ]
	except:
		print("non numeric publisher list supplued with -l option")
		quit(1)
	list_set = set(list)
	subset = list_set.intersection(cmd_list)
	list = [ int( item) for item in subset ]

# Get the authentication for this session
# from authenticationSupport import get_auth_token
auth_struct = get_auth_structure()

account_to_fileid_mapping = {}

# Now we have set up the publishers and have the fildid_dict in place
#=========================================
# upload and run reports
#=========================================

fileid_dict,auth_struct = upload_and_run_reports_for_list(auth_struct,list,args,verbose=verbose)

if fileid_dict != {}:
	fileid_dict,auth_struct = fetch_report_runs(fileid_dict,auth_struct,write_to_database=write_to_database,write_to_file=write_to_file)
	
	sleep_time = 10
	for count in range(0,max_retries):
		from time import sleep
		fileid_dict,auth_struct = fetch_report_runs(fileid_dict,auth_struct,write_to_database=write_to_database,write_to_file=write_to_file)
		if len(fileid_dict) == 0:
			break
		else:
			sleep(sleep_time)
if activity_report == True:
	print("Activity report for Index Exchange to MySQL DB download")
	print(len(list)," publishers processed for ",len(args),"reports")
	if len(fileid_dict)!=0:
		print("")
# finally also do the command line args
if len(fileid_dict)!=0:
	if poduce_outcome_report == True:
		print("File ID downloads incomplete:")
		for id in fileid_dict.keys():
			print("file download",id,"for publisher",fileid_dict[id]['publisher'])
		print("value of retries is", max_retries)
