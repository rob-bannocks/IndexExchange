# settings.py
import os
# import settings # for latter use
from os.path import join, dirname
from dotenv import load_dotenv,dotenv_values
from pathlib import Path
from os.path import exists

# to avoid sharing auth secrets on github include a .gitignore with a line specifiying .env-secrets.
def get_secrets_filepath():
	SECRETSFILE='.env-secrets'
	return os.path.join(os.path.expanduser('~'), SECRETSFILE)

def get_var_from_sec_file_or_none(variablename):
	try:
		config = dotenv_values(get_secrets_filepath())
	except:
		return None

	try:
		varname = config[variablename]
	except:
		return None

	return varname

def get_var_from_env_or_sec_file(variablename):
	varname = os.environ.get(variablename)
	# if not in the environment then read from the auth file.
	if varname == None:
		dotenv_path = get_secrets_filepath()
		try:
			config = dotenv_values(dotenv_path)
		except:
			print(variablename," not configured in environment and no "+dotenv_path+" file")
			quit(1)
		try:
			varname = config[variablename]
		except:
			print(variablename," not specified in environment nor "+dotenv_path+" in variable INDEXEXCHANGEUSERNAME")
			quit(1)

	return varname

def getEmail_env_var():
	return "INDEXEXCHANGEUSERNAME"

def getEmail():
	variablename = getEmail_env_var()
	return get_var_from_env_or_sec_file(variablename)

def getEmail_or_none():
	variablename = getEmail_env_var()
	return get_var_from_sec_file_or_none(variablename)

def getPassword_env_var():
	return "INDEXEXCHANGEPASSWORD"

def getPassword():
	variablename = getPassword_env_var()
	return get_var_from_env_or_sec_file(variablename)

def getPassword_or_none():
	variablename = getPassword_env_var()
	return get_var_from_sec_file_or_none(variablename)

def get_data_download_store():
    dir = os.path.join(get_product_root(),"INDEX-DATA-DOWNLOAD")
    Path(dir).mkdir(parents=True,exist_ok=True)
    return dir

def get_templates_store():
    dir = os.path.join(get_product_root(),"INDEX-TEMPLATES")
    Path(dir).mkdir(parents=True,exist_ok=True)
    return dir
# templates for uploaded reports to be run

# Functions to read accounts store in python
# no longer used
def get_product_root():
    """
    This function returns the root of the product, where the .enc-secrets file and the
    various data, report, and spool directories are kept.
    
    """
    PRODUCTROOTSTRING='~' # Change if you want to modify
    return os.path.expanduser(PRODUCTROOTSTRING)

def get_report_runs_download_queue():
    dir = os.path.join(get_product_root(),"INDEX-REPORT-RUNS-DOWNLOAD-QUEUE")
    Path(dir).mkdir(parents=True,exist_ok=True)
    return dir

def get_reports_to_be_run_queue():
    dir = os.path.join(get_product_root(),"INDEX-REPORTS-TO-BE-RUN-QUEUE")
    Path(dir).mkdir(parents=True,exist_ok=True)
    return dir

def get_mysql_username_env_var():
	return "SALESMYSQLUSERNAME"

def get_mysql_username():
	variablename = get_mysql_username_env_var()
	return get_var_from_env_or_sec_file(variablename)

def get_mysql_username_or_none():
	variablename = get_mysql_username_env_var()
	return get_var_from_sec_file_or_none(variablename)

def get_mysql_password_env_var():
	return "SALESMYSQLPASSWORD"

def get_mysql_password():
	variablename = get_mysql_password_env_var()
	return get_var_from_env_or_sec_file(variablename)

def get_mysql_password_or_none():
	variablename = get_mysql_password_env_var()
	return get_var_from_sec_file_or_none(variablename)
	
def get_mysql_hostname_env_var():
	return "SALESMYSQLHOSTNAME"

def get_mysql_hostname():
	variablename = get_mysql_hostname_env_var()
	fromfile = get_var_from_sec_file_or_none(variablename)
	if fromfile == None:
		return "localhost"
	else:
		return fromfile
	
def get_index_exchange_settings_dir():
    dir = os.path.join(get_product_root(),"INDEX-SETTINGS")
    Path(dir).mkdir(parents=True,exist_ok=True)
    return dir

def report_settings_overrides():
	dict = {}
	return dict

def get_mysql_db_name():
	return "prog_stats"

def get_fileid_table_name():
	return "prog_ix_fileid"

def get_reportid_table_name():
	return "prog_ix_reportid"

def get_version():
	return "1.0"

if __name__ == "__main__":
	print("The secrets file is",get_secrets_filepath())
	print("The email address is "+str(getEmail()))
	print("The password is "+getPassword())
	print("The report template directory is",get_templates_store())
	print("The report runs data download directory is ", get_data_download_store())

	print("The publishers file is ",get_accountids_file())
	print("The publishers account id store dir is ",get_product_root())
	print("The final publishers filepath is ", get_accountids_filepath())
	print("The download report runs queue is ", get_report_runs_download_queue() )
	print("The report run queue is ",get_reports_to_be_run_queue() )
	print("The MySQL database username is ",get_mysql_username())
	print("The MySQL database password is ",get_mysql_password())
	print("The MySQL hostname is ",get_mysql_hostname())
	print("Settings dir is ", get_index_exchange_settings_dir())
