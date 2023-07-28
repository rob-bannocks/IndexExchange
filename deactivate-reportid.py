# deactivate-reports.py

from reportmanagementAPI import api_deactivate_report
from authenticationSupport import get_auth_token
import getopt
import sys

debug = False

def usage():
    print(sys.argv[0],"[-h|--help] [-D] reportID [ reportID ]")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hD", ["help", "debug"]) 
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
    else:
        assert False, "unhandled option"

if len(args) == 0:
	usage()
	quit(1)
num_array=[int(i) for i in args ]
if num_array == []:
    num_array = None

auth_token = get_auth_token()
if num_array != None:
	new_dict = {}
	for reportID in num_array:
		if debug == True:
			print("API call to deactivete ",reportID)
		response = api_deactivate_report(auth_token,reportID)
		if debug == True:
			print("response status code is ",response.status_code)
			print("response content is ",response.content)
