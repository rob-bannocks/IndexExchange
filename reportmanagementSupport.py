# reportmanagementSupport.py
# This file contains functions to manipulate the Index Exchange API.  They all require a
# auth_token which authenticates the connection.  Functions in authenticationSupport.py can generate
# this most notably get_auth()
from authenticationSupport import get_auth_token
import requests
from json import loads
from reportmanagementAPI import api_run_adhoc_report_to_download,api_list_specific_report,api_create_report ,api_list_active_reports
from reportdownloadAPI import api_download_a_report_file
from reportmanagementAPI import  api_update_report

################################################################### Support Functions #####################
###
### Support functions
###
from utility import generate_unique_report_name
from readwrite import get_report_from_local_store
def get_specific_report_as_dict(auth_struct,reportid):
	# ensure tokem current
	auth_struct = renew_auth_structure(auth_struct)
	auth_token = return_auth_token_from_auth_struct(auth_struct)

	downloadedreport= api_list_specific_report(auth_token,reportid)
	if downloadedreport != None:
		return loads(downloadedreport.content.decode())
	else:
		return None

def get_specific_report_in_json(reportid):
	response_token=get_auth_token()
	#downloadedreport=get_specific_report(response_token,reportid)
	downloadedreport= api_list_specific_report(response_token,reportid)
	if downloadedreport != None:
		return downloadedreport.json()
	else:
		return None

def return_upload_report_headers(auth_token):
	headers = {
		"accept": "application/json",
		"Authorization": "Bearer "+str(auth_token),
		"content-type": "application/json"
	}
	return headers

def return_report_upload_payload(accountids,report_name,report_json,returnfiletype,feilds,filters,dateRange,schedule,startDate=None,endDate=None,delivery=None):
	if returnfiletype != None:
		payload["fileType"] = "csv"
  
	payload = {
		"accounts" : "["+accountids+"]",
		"fileType" : returnfiletype,
		"reportTitle" : report_name,
		"querySpec" : report_json, # DOUBLE CHECK THE FORMAT NEEDED HERE
		}

	if feilds != None:
		payload["feilds"] = feilds
	if filters != None:
		payload["filters"] = filters

	return payload
	
def report_enforce_settings(report_dict):
	"""
	
	this is a function to consistently enforce some settings in reports uploaded or updated.
	At present this is only the regionSetting which forces all reports to UTC and a fixed
	number of columns in the subsequent fileID download.
	"""
	report_dict["regionSetting"] = "standard"

	return report_dict

def create_or_upload_process_args(report_dict,accountIDs,accountGroupID=None,regionSetting=None,fileType="csv",delivery=None,querySpec=None,dateRange=None,schedule=None,startDate=None,endDate=None):
	report_dict["accounts"] = accountIDs
	if accountGroupID != None:
		report_dict["accountGroupID"] = accountGroupID
	if regionSetting != None:
		report_dict["regionSetting"] = regionSetting
	if fileType != None:
		report_dict["fileType"] = fileType
	if delivery != None:
		report_dict["delivery"] = delivery
	if querySpec != None:
		report_dict["querySpec"] = querySpec
	if dateRange != None:
		report_dict["daterange"] = dateRange
	if schedule != None:
		report_dict["schedule"] = schedule
	if startDate != None:
		report_dict["startDate"] = startDate
	if endDate != None:
		report_dict["endDate"] = endDate

	report_dict = report_enforce_settings(report_dict)

	return report_dict

def upload_existing_report(auth_token,accountIDs,report_name,accountGroupID=None,regionSetting=None,fileType="csv",delivery=None,querySpec=None,dateRange=None,schedule=None,startDate=None,endDate=None,stop_on_error=True):
	"""
	This function uploads an existing report in the local (file) store.  It modifies the relevent parts
	at minumum - the title, accountIDs, return
		report_name - filename - filename of the report spec file, whcih is a JSON file, in the local store
		accountIDs - list of ints - This parameter is mandatory.  It is an intefer list of the accounts
		fileType - a string - by default this is set to "csv" no matter what the local report says, however,
		it can be omitted by setting it to None in the function call or a string which is one of "csv", 
		"csv.gz", or "csv.zip".
			to apply this report to
		Other settings are as per the spec at api.indexchanage.com.  These are only modified if specified
		in the function call.
 	"""
	if not isinstance(accountIDs, list):
		print("Error accountIDs must be a one element list, even if it has only one entry.")
		quit(1)

	upload_report_url = "https://app.indexexchange.com/api/reporting/agg/v1/report-specs"

	report_upload_name = report_name +" taken from template " +generate_unique_report_name()
	report_json = get_report_from_local_store(report_name)
	report_json_upload = report_json['reportDefinition']
 
	report_json_upload["reportTitle"] = report_upload_name

	report_json_upload = create_or_upload_process_args(report_json_upload,accountIDs,accountGroupID,regionSetting,fileType,delivery,querySpec,dateRange,schedule,startDate,endDate)

	# construct headers
	headers = return_upload_report_headers(auth_token)
	# construct payload
	reportID = api_create_report(auth_token,report_json_upload,stop_on_error=stop_on_error)

	if stop_on_error == True:
		return reportID
	else:
		if reportID.status_code != 201:
			print("[upload_existing_report] fails for report name",report_name,"with return code",reportID.status_code,"reason",reportID.reason,"for report",report_name,"and account",accountIDs)
			return None
	result_report_j=loads(reportID.content.decode())
	result_report_int = result_report_j["reportSpecID"]

	return result_report_int

def update_existing_report(auth_token,accountID,reportID,report_name,accountGroupID=None,regionSetting=None,fileType="csv",delivery=None,querySpec=None,dateRange=None,schedule=None,startDate=None,endDate=None,stop_on_error=True):
	"""
	This function uploads an existing report in the local (file) store.  It modifies the relevent parts
	at minumum - the title, accountID, return
		report_name - filename - filename of the report spec file, whcih is a JSON file, in the local store
		accountID - list of ints - This parameter is mandatory.  It is an intefer list of the accounts
		fileType - a string - by default this is set to "csv" no matter what the local report says, however,
		it can be omitted by setting it to None in the function call or a string which is one of "csv", 
		"csv.gz", or "csv.zip".
			to apply this report to
		Other settings are as per the spec at api.indexchanage.com.  These are only modified if specified
		in the function call.
 	"""
	reportID = int(reportID)

	if not isinstance(accountID, list):
		print("Error accountID must be a one element list, even if it has only one entry.")
		quit(1)

	report_upload_name = report_name +" UPDATED taken from template " +generate_unique_report_name()
	report_json = get_report_from_local_store(report_name)
	report_json_upload = report_json['reportDefinition']
 
	report_json_upload["reportTitle"] = report_upload_name

	report_json_upload = create_or_upload_process_args(report_json_upload,accountID,accountGroupID,regionSetting,fileType,delivery,querySpec,dateRange,schedule,startDate,endDate)

	# construct headers
	headers = return_upload_report_headers(auth_token)

	reportID = api_update_report(auth_token,reportID,report_json_upload,stop_on_error=stop_on_error)

	if stop_on_error == True:
		return reportID
	else:
		if reportID.status_code != 200:
			print("[update_existing_report] fails for report name",report_name,"with return code",reportID.status_code,"reason",reportID.reason,"for report",report_name,"and account",accountID)
			return None
	result_report_j=loads(reportID.content.decode())
	result_report = result_report_j["success"]

	return result_report
	
###
def run_adhoc_report_to_download(auth_token,result_report_int):
	fileid_json = api_run_adhoc_report_to_download(auth_token,result_report_int)
	fileid_int = int(fileid_json["reportRunID"])
	return fileid_int

def get_list_int_active_reports(auth_token,accountIDs=None,accountGroupIDs=None):
	result = api_list_active_reports(auth_token,accountIDs=None,accountGroupIDs=None)
	if result.status_code != 200:
		print("Index Exchange returns error for list of active report IDs")
		quit(1)
	# get content and transform to list.
	return_list = loads(result.content.decode())
	try:
		return_new_list = list([ item['reportID'] for item in return_list ])
	except:
		print("running: return_new_list = list([ item['reportID'] for item in return_list ]) fails")
		print("item:",item,"return_list",return_list)
		quit(1)

	return return_new_list
	
if __name__ == "__main__":
	# settings.py
	print("Tests")
	auth_token = get_auth_token()
	list = get_list_int_active_reports(auth_token)
	print(type(list))
	print(list)
	print("-------")
	# print(response_token)
	def test_get_list_reports():
		accountID="190680"

		report_list_json = get_list_reports(response_token)
		print(report_list_json.text)
	#print("----")
	def test_get_specific_report(reportid):
		response_token=get_auth_token()
		downloadedreport=get_specific_report(response_token,reportid)
		print(type(downloadedreport.json()))
		print(downloadedreport.text)
 
	def local_upload_report(report_name="new3",	accountIDs=[190680]):
		print("Sending report",report_name," for accountIDs ",accountIDs)
		#result_report_j=loads(upload_existing_report(auth_token,accountIDs,report_name,fileType="csv").decode())
		#result_report_int = result_report_j["reportSpecID"]
		#return result_report_int
		return upload_existing_report(auth_token,accountIDs,report_name,fileType="csv")
	result_report_int = local_upload_report()
	# construct payload
	#print("payload = ",return_report_upload_payload("1191494","testing","{JSON{}}"),returnfiletype="csv",feilds=None,filters=None,dateRange=None,schedule=None,startDate=None,endDate=None,delivery=None)
	#json_list = list_avaliable_files(auth_token)
	#print(dumps(json_list.json()))
	
	def local_run_report(result_report_int):
		print("upload_existing_report reports report spec as ", result_report_int," running this report")
		fileid_json = api_run_adhoc_report_to_download(auth_token,result_report_int)
		print("run or report ",result_report_int,"	 returns-->",fileid_json)
		fileid_int = int(fileid_json["reportRunID"])
		return fileid_int
	fileid_int = local_run_report(result_report_int)	
	#print(fileid_int)
	print("fileID is ",fileid_int, "print collecting this run results")
	file = api_download_a_report_file(auth_token,str(fileid_int))
	print("here is the file:")
	print(file)

	for i in range(0,9000):
		auth_token = get_auth_token()
		print(get_list_avaliable_fileIDs(auth_token))
		print("n is ",i,"connection auth life time ",ic.get_token_expiry_time()," time now ",datetime.datetime.now().strftime('%Y %m %d %H:%M:%S'))
		print("List of file IDs ",get_list_avaliable_fileIDs(ic.get_connection(),status = "downloaded"))
