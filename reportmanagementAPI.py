# reports.py
# This file contains functions to manipulate the Index Exchange API.  They all require a
# auth_token which authenticates the connection.  Functions in authenticationSupport.py can generate
# this most notably get_auth()
from authenticationSupport import get_auth_header,get_auth_update_report_header
import requests
from json import dumps,loads
from urlencoding import list_int_to_urlstring, int_to_urlstring
#from ast.byte_str import decode

################################################################### API Functions #########################
###
### API Functions
###

#def create_report(auth_token,accountIDs,accountGroupID=None,regionSetting=None,fileType="csv",delivery=None,querySpec=None,dateRange=None,schedule=None,startDate=None,endDate=None):

def api_create_report(auth_token,payload,stop_on_error=True):
	url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs"

	# it is important that the accountIDs are a list.  Due to a current limitation of Index Exchange
	# this can only be a one element list.
	#if not isinstance(accountIDs, list):
	#	print("Error accountIDs must be a one element list, even if it has only one entry.")
	#	quit(1)

	headers = get_auth_header(auth_token)

	response = requests.post(url, headers=headers, json=payload)

	if stop_on_error == True:
		if response.status_code != 201:
			SystemExit("Report fetch failed",response.status_code,"reason",response.reason)		
			print("[api_create_report] fails with return code",response.status_code,"reason",response.reason)
			quit(1)

		result_report_j=loads(response.content.decode())
		result_report_int = result_report_j["reportSpecID"]

		return result_report_int
	else:
		return response

def api_list_active_reports(auth_token,accountIDs=None,accountGroupIDs=None):
	"""
	This function uses the API to get a list of avaliable reports.  accountIDs must be a list even if it is a simgle valued list
	accountGroupIDs is a single value.
	"""
	# check accountIDs is a list
	if accountGroupIDs == None:
		if accountIDs == None:
			list_active_reports_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/info"
		else:
			list_active_reports_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/info?accountIDs="+list_int_to_urlstring(accountIDs)
	else:
		if accountIDs == None:
			list_active_reports_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/info?accountGroupIDs="+accountGroupIDs
		else:
			list_active_reports_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/info?accountIDs="+list_int_to_urlstring(accountID)+"&accountGroupIDs="+accountGroupIDs
	
	headers = get_auth_header(auth_token)

	report_response = requests.get(list_active_reports_url, headers=headers)

	return report_response


def get_specific_report(auth_token,reportID):
	return api_list_specific_report(auth_token,reportID)

def api_list_specific_report(auth_token,reportID):
	"""
	This function uses the IndexExchange REST API to fetch a JSON object which describes a report.

	Args:
		reportID (string): the ID of the report from Index Exchange
  	"""
	get_specific_report_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/json/"+int_to_urlstring(reportID)

	headers = get_auth_header(auth_token)

	response = requests.get(get_specific_report_url, headers=headers)
	if response.status_code != 200:
		print("[get_specific_report] fetch report fails for report", reportID,"with response code",response.status_code)
		SystemExit("Report fetch failed",response.status_code)		
		return None
	return response

def api_update_report(auth_token,reportID,payload,stop_on_error=True):
	# it is important that the accountIDs are a list.  Due to a current limitation of Index Exchange
	# this can only be a one element list.

	url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/"+ int_to_urlstring(reportID)
	
	headers = get_auth_update_report_header(auth_token)
	
	response = requests.patch(url, headers=headers, json=payload)
	if stop_on_error == True:
		if response.status_code != 200:
			SystemExit("Report fetch failed",response.status_code,"reason",response.reason)		
			print("[api_create_report] fails for report name",accountIDs,"with return code",response.status_code,"reason",response.reason)
			quit(1)

		result_report_j=loads(response.content.decode())
		result_report_int = result_report_j["reportSpecID"]

		return result_report_int
	else:
		return response

def api_deactivate_report(auth_token,reportID):
	url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/"+int_to_urlstring(reportID)+"/deactivate"

	headers = get_auth_header(auth_token)

	return requests.put(url, headers=headers)

def api_run_adhoc_report_to_download(auth_token,reportid):
	"""
	This function runs the run adhoc report to download

	Args:
		reportid (_type_): an authentication token taken from a sucessfull authentication request sent via the api_generate_user_account_token
	"""
    
	url = "https://app.indexexchange.com/api/reporting/agg/v1/report-runs"

	# import requests
	payload = {"reportID": int(reportid)}
	headers = get_auth_header(auth_token)

	response = requests.post(url, json=payload, headers=headers)
	if response.status_code != 201:
		print("[api_run_adhoc_report_to_download] returns error ",response.status_code," ",response.content)
		quit(1)
	return_val=loads(response.content)
 
	return return_val

def api_run_adhoc_report_to_email(auth_token,reportID,recipientsArray):
	"""
		This function implements the List Active Reports Prog API
	"""
	url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs/"+int_to_urlstring(reportID)+"run"
	
	if type(recipientsArray) is not list :
		print("[api_run_adhoc_report_to_email] must be called with an array of recipients even if there is only one")
		quit(1)
	
	payload = {"recipients": recipientsArray }
	headers = get_auth_header(auth_token)

	response = requests.post(url, json=payload, headers=headers)
	if response.status_code != 201:
		print("[api_run_adhoc_report_to_download] returns error ",response.status_code," ",response.content)
		quit(1)
 
	return response.content

if __name__ == "__main__":
	from authenticationSupport import get_auth_token,extract_auth_token_value,get_auth
	# settings.py
	print("Tests")
	auth_token = get_auth_token()
	def test_get_list_reports():
		accountID="190680"

		report_list_json = get_list_reports(response_token)
		print(report_list_json.text)
	def test_get_specific_report(reportid):
		#response_token=extract_auth_token_value(get_auth())
		response_token=get_auth_token()
		downloadedreport=get_specific_report(response_token,reportid)
		print(type(downloadedreport.json()))
		print(downloadedreport.text)
 
	def local_upload_report(report_name="new3",	accountIDs=[190680]):
		from reportmanagementSupport import upload_existing_report
		print("Sending report",report_name," for accountIDs ",accountIDs)
		#result_report_j=loads(upload_existing_report(auth_token,accountIDs,report_name,fileType="csv").decode())
		#result_report_int = result_report_j["reportSpecID"]
		#return result_report_int
		return upload_existing_report(auth_token,accountIDs,report_name,fileType="csv")
	result_report_int = local_upload_report()
	# construct payload
	
	def local_run_report(result_report_int):
		from reportmanagementSupport import upload_existing_report
		print("upload_existing_report reports report spec as ", result_report_int," running this report")
		fileid_json = api_run_adhoc_report_to_download(auth_token,result_report_int)
		print("run or report ",result_report_int,"	 returns-->",fileid_json)
		fileid_int = int(fileid_json["reportRunID"])
		return fileid_int
	fileid_int = local_run_report(result_report_int)	
	print("fileID is ",fileid_int, "print collecting this run results")
	from reportdownloadAPI import api_download_a_report_file
	file = api_download_a_report_file(auth_token,str(fileid_int))
	print("here is the file:")
	print(file)

	for i in range(0,9000):
		auth_token = get_auth()
		print(get_list_avaliable_fileIDs(auth_token))
		print("n is ",i,"connection auth life time ",ic.get_token_expiry_time()," time now ",datetime.datetime.now().strftime('%Y %m %d %H:%M:%S'))
		print("List of file IDs ",get_list_avaliable_fileIDs(ic.get_connection(),status = "downloaded"))
