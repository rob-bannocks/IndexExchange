# reports.py
# This file contains functions to manipulate the Index Exchange API.  They all require a
# auth_token which authenticates the connection.  Functions in authenticationSupport.py can generate
# this most notably get_auth()
from authenticationSupport import get_auth_header
from authenticationSupport import get_auth_token
from urlencoding import string_to_urlstring
from json import dumps,loads
from urlencoding import list_int_to_urlstring,string_to_urlstring
import requests

def api_list_avaliable_files(auth_token,fileIDs=None,accountIDs=None,status=None):
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
		JSON report listing the avaliable files or an error.
	"""
	base_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-files/list"
	if accountIDs == None and fileIDs == None and status == None:
		pass
	else:
		ampersand=False
		base_url += "?"
		if accountIDs != None:
			base_url += "accountIDs="+list_int_to_urlstring(accountIDs)
			ampersand = True
		if fileIDs != None:
			if ampersand == True:
				base_url += "&"
			ampersand = True		
			base_url += "fileIDs="+list_int_to_urlstring(fileIDs)
		if status != None:
			if ampersand == True:
				base_url += "&"
			base_url += "status="+status			
   
	headers = get_auth_header(auth_token)	

	response = requests.get(base_url, headers=headers)
	return response.content

def api_download_a_report_file(auth_token,fileID,stop_on_error=True):
	"""
	This function downlaods a "report file" which means an instance of a report run.  It uses the
	Index Exchange REST API to fetch the file

	this function gets a copy of a report (The JSON) and returns it.
	NB this does not RUN the report.  see run_adhos_report_to_download() for that
	"""

	# url
	fetch_report_base_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-files/download/"+string_to_urlstring(fileID)

	# get auth_heaer
	headers = get_auth_header(auth_token)

	response = requests.get(fetch_report_base_url, headers=headers)
	if stop_on_error == True:
		if response.status_code != 200:
			print("[api_download_a_report_file] returns error ",response.status_code," ",response.content)
			quit(1)

		return response.content
	else:
		# NB different functionality if stop_on_error is different, we return the whole response
		# not just the content
		return response
