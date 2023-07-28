# crete-env-secrets-store.py program

# call functions in reports.py to get and save a report.
from settings import getEmail_or_none,getPassword_or_none,get_mysql_username_or_none,get_mysql_password_or_none,get_mysql_hostname
from settings import getEmail_env_var, getPassword_env_var, get_mysql_username_env_var, get_mysql_password_env_var, get_mysql_hostname_env_var
from settings import get_secrets_filepath
from getopt import getopt
import sys

def usage():
    print(sys.argv[0],"[-h|--help] [-s] [-u index-exchange-username ] [ -p index-exchange-password ] [-P MySQL-Password ] [-m MySQL-Username ] [ -H MySQL-HOST ] [ Index-Exchange-username [index-exchange-password [MySQL-Username [MySQL-Password [ MySQL-HOST ]]]]] ")
# get report from command line
try:
    opts, args = getopt(sys.argv[1:], "hDu:p:P:m:H:s", ["help", "Debug","INDEX-EXCHANGE-USERNAME","INDEX-EXCHANGE-PASSWORD=","MySQL-Password=","MySQL-Username=","MySQL-Host="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
    # store report
# set up defaults
verbose=False
debug=False
run_with_zero_args = False
silent = False
# proccess options    
# unusually the args are pseudo options
ENVSECFILEPATH=get_secrets_filepath()
EMAILV = getEmail_or_none()
PASSV = getPassword_or_none()
MYSQLUV = get_mysql_username_or_none()
MYSQLPV = get_mysql_password_or_none()
MYSQLHV = get_mysql_hostname()
n_args = len(args)
if n_args >5:
	usage()
	quit(1)
elif n_args == 6:
        MYSQLHV = args[5]
        CALAPIKEYV = args[4]
        MYSQLPV = args[3]
        MYSQLUV = args[2]
        PASSV = args[1]
        EMAILV = args[0]
elif n_args == 5:
        MYSQLHV = args[4]
        MYSQLPV = args[3]
        MYSQLUV = args[2]
        PASSV = args[1]
        EMAILV = args[0]
elif n_args == 4:
        MYSQLPV = args[3]
        MYSQLUV = args[2]
        PASSV = args[1]
        EMAILV = args[0]
elif n_args == 3:
        MYSQLUV = args[2]
        PASSV = args[1]
        EMAILV = args[0]
elif n_args == 2:
        PASSV = args[1]
        EMAILV = args[0]
elif n_args == 1:
        EMAILV = args[0]
	
for o, a in opts:
    if o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-u",):
        EMAILV = a
    elif o in ("-p",):
        PASSV = a
        run_with_zero_args = True
    elif o == "-P":
        MYSQLPV = a
        run_with_zero_args = True
    elif o == "-m":
        MYSQLUV = a
        run_with_zero_args = True
    elif o == "-H":
        MYSQLHV = a
        run_with_zero_args = True
    #elif o == "-k":
    #    CALAPIKEYV = a
        run_with_zero_args = True
    elif o == "-s":
        silent = True
        run_with_zero_args = True
    else:
        assert False, "unhandled option"

def print_current_values():
	print("Current Settings:")
	print("Index Exchange username/email:", getEmail_or_none())
	print("Index Exchange password:", getPassword_or_none())
	print("MySQL username:", get_mysql_username_or_none())
	print("MySQL password:", get_mysql_password_or_none())
	print("MySQL hostname:", get_mysql_hostname())

if n_args == 0 and run_with_zero_args == False:
	print_current_values()
	#usage()

elif len(args) >6:
	print("Error maximum 5 non-option args")
	usage()
	quit(1)
else:
	filename = get_secrets_filepath()
	EMAIL=getEmail_env_var()
	PASS=getPassword_env_var()
	MUSER=get_mysql_username_env_var()
	MPASS=get_mysql_password_env_var()
	MHOST=get_mysql_hostname_env_var()
	if silent != True:
		if EMAILV != None:
			print(EMAIL+"='"+EMAILV+"'")
		if PASSV != None:
			print(PASS+"='"+PASSV+"'")
		if MYSQLUV != None:
			print(MUSER+"='"+MYSQLUV+"'")
		if MYSQLPV != None:
			print(MPASS+"='"+MYSQLPV+"'")
			print(MHOST+"='"+MYSQLHV+"'")
	with open(filename, "w") as f:
		if EMAILV != None:
			f.write(EMAIL+"='"+EMAILV+"'\n")
		if PASSV != None:
			f.write(PASS+"='"+PASSV+"'\n")
		if MYSQLUV != None:
			f.write(MUSER+"='"+MYSQLUV+"'\n")
		if MYSQLPV != None:
			f.write(MPASS+"='"+MYSQLPV+"'\n")
		if MHOST != None:
			f.write(MHOST+"='"+MYSQLHV+"'\n")
		f.close()

# get the file name
if debug == True:
    print("end of program")
