# reportdownloadSupport.py
# These functions use reportdownloadAPI adding functionality to the raw API
# some all require an auth_token which authenticates the connection.  Functions
# in authenticationSupport.py can generate this most notably get_auth_token()

from authenticationSupport import get_auth_header
from authenticationSupport import get_auth_token
from json import dumps,loads
from reportdownloadAPI import api_list_avaliable_files
from reportdownloadAPI import api_download_a_report_file
from settings import get_data_download_store

# 
# support functions
#
def get_list_avaliable_files_json(auth_token,fileIDs=None,accountIDs=None,status=None):
	"""
	Input parameters:
		auth_token - an authentication token
		status - a string one of "new","downloaded" or None for both - Filters
			the report by the API download status, where: 
				new = you have not downloaded the report using the API. 
				downloaded = you have downloaded the report using the API.
				If omitted, both downloaded and new reports will appear.
		fileIDs - a string - A comma separated list of the unique IDs associated
  			with the files that you want to retrieve. 
			Note: You can find the fileID at the end of the downloadURL returned
   			in the Download a report file route response.
		accountIDs - an integer list - A comma seperated list of accountIDs for the
  			files that you want to see. 
     		If omitted, all reports associated your accounts will appear.
	Returns:
		a list of avalible fileIDs matching the parametes
  	"""
	json_return = loads(api_list_avaliable_files(auth_token,fileIDs,accountIDs,status).decode())

	return json_return

def get_list_avaliable_fileIDs(auth_token,fileIDs=None,accountIDs=None,status=None):
	json = get_list_avaliable_files_json(auth_token,fileIDs=None,accountIDs=None,status=None)
	return return_list_of_specific_fileIDs(json)

def return_list_of_specific_fileIDs(json):
	return [ item["fileID"] for item in json]

def get_a_report_run(auth_token,fileID,stop_on_error=True):
    # file = get_download_a_report_file(fileID)
    response = api_download_a_report_file(auth_token,str(fileID),stop_on_error=stop_on_error)
    if stop_on_error == True:
        # this is still a decoded response so return in full
        return response
    else:
     return response # api in this case will have ended program flow

def get_a_report_run_or_null(auth_token,fileID,stop_on_error=True):
    response = get_a_report_run(auth_token,fileID,stop_on_error=stop_on_error)
    if stop_on_error == True:
        return response # if error api_ will have stopped program flow in this case
        # this will be a requests decoded response
    else:
	# below needs modification as we will not get here unless the response.status_code is 200.
        if response.status_code != 200:
         return None
        else:
         return response # which should be a decoded file
