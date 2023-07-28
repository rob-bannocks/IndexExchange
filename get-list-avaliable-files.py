# api_list_avaliable_files.py
from reportdownloadAPI import api_list_avaliable_files,api_download_a_report_file
from authenticationSupport import get_auth_token
import utility
from json import dumps,loads
import getopt
import sys
auth_token = get_auth_token()
debug = False

def usage():
    print(sys.argv[0],"[-h|--help] [-i indent ] [-j] fileID [fileID]")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hvDs:ji:", ["help","verbose", "debug", "status=", "fileIDs=", "json","indent="]) 
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
indent=8
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
    elif o == "-s":
        status = a
    elif o == "-j":
        json = True
    elif o == "-i":
        indent = int(a)
    else:
        assert False, "unhandled option"

num_array=[int(i) for i in args ]
if num_array == []:
	num_array = None

if debug == True:
    print(str(str1))
    print("========")

list = api_list_avaliable_files(auth_token,fileIDs=num_array,accountIDs=accountIDs,status=status).decode()
list_dict = loads(list)

list_int = [ item["fileID"] for item in list_dict ]

if debug == True:
	for ele in args:
		if int(ele) in list_int:
			print("found ",ele)
		else:
			print("not found ", ele)

if json != True:
	print(sorted(list_int))
else:
	if debug == True:
		print(list)
		rint("------")
	print(dumps(list_dict ,indent=indent))
if debug == True:
	print(num_array)
