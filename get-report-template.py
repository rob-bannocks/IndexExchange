# get-report-template utility program
#
#

# call functions in reports.py to get and save a report.
from settings import get_templates_store
import getopt
import sys
from readwrite import save_specific_report_in_json

def usage():
    print(sys.argv[0],"[-h|--help] [ -n ] [-o output] [-d directory] repordid1 reportid2 ....")
# get report from command line
try:
    opts, args = getopt.getopt(sys.argv[1:], "hnDd:o:v", ["help", "use report number for file name","output=","verbose"])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    # store report
# set up defaults
store_dir = get_templates_store()
verbose=False
debug=False
use_report_number_for_filename=False
# proccess options    
for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-o", "--output"):
        output = a
    elif o == "-d":
        store_dir = a
    elif o == "-D":
        debug=True
        print("debugging on")
    elif o == "-n":
        use_report_number_for_filename=True
    else:
        assert False, "unhandled option"

for ele in args:
    if debug == True:
        print("Doing report ",ele)
    if use_report_number_for_filename == True:
      save_specific_report_in_json(ele,use_report_number=use_report_number_for_filename,verbose=verbose )
    else:
      save_specific_report_in_json(ele,use_report_number=use_report_number_for_filename,verbose=verbose )
    if verbose == True:
        print("report",ele)
