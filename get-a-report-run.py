#!python3
# api_list_avaliable_files.py
from reportdownloadAPI import api_list_avaliable_files,api_download_a_report_file
from reportdownloadSupport import get_a_report_run_or_null
from authenticationSupport import get_auth_token
from readwrite import write_list_to_csv_file

import utility
from json import dumps
import getopt
import sys
from json import loads
auth_token = get_auth_token()
debug = False
from settings import get_data_download_store
directory= get_data_download_store()

def usage():
    print(sys.argv[0],"[-h|--help] [ -p publisher ] [-j] [ -s status ] [-d directory] [-D] fileID [ fileID ]")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hp:vDd:js:", ["help","verbose", "debug", "directory=", "json", "status"]) 
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
status = None
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
    elif o == "-d":
        directory = a
    elif o == "-p":
        publisher =a
    elif o == "-j":
        json = True
    elif o == "-s":
        status = a
    else:
        assert False, "unhandled option"

num_array=[int(i) for i in args ]
if num_array == []:
    num_array = None

list = api_list_avaliable_files(auth_token,fileIDs=num_array,accountIDs=accountIDs,status=status).decode()
list_json = loads(list)

list_int = [ item["fileID"] for item in list_json]

for ele in args:
	fileID=int(ele)
	if fileID in list_int:
		if debug == True:
			print("found ",ele)
		file = get_a_report_run_or_null(auth_token, fileID=fileID,stop_on_error=False)
		#if debug == True:
		if file == None:
			print("none returned")
		else:
			print("File is :")
			print(file.content.decode())
			#write_list_to_csv_file(file)
			write_list_to_csv_file(str(id),csv)
	else:
		print("not found ", ele)

if debug == True:
	if json == True:
		print("======")
		print(sorted(list_int))
	else:
		print("======")
		print(list)
		print("======")
		print(list_json)
	if debug == True:
		print("______")
		print(num_array)
