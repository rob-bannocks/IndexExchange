# Log retrieval.py
#
# API functions to interact with the Log retrieval CAL API at Index Exchange
#

from requests import get
from calcoreAPI import calcoreget_no_payload,headers_calAPI

def download_log_file_stem():
	return "https://app.indexexchange.com/api/cal/v1/files/" 

def download_log_file_url():
	return download_log_file_stem()+"file_id"

def bid_event_logs_API(access_token,url = "https://app.indexexchange.com/api/cal/v1/downloads/bidevents"):
	return calcoreget_no_payload(access_token,url)

def impression_event_logs_API(access_token, url = "https://app.indexexchange.com/api/cal/v1/downloads"):
	return calcoreget_no_payload(access_token,url)

def headers_download_calAPI(access_token):
	headers = headers_calAPI(access_token)
	#headers['access_token'] : access_token

	return headers

def download_log_file_payload(fileid):
	payload = {
		"file_id": str(fileid)
	}
	
	return payload

def download_log_file_via_url_API(access_token,url):
	#return core_download_log_file(access_token,url)

	headers = headers_download_calAPI(access_token)

	response = get(url,headers=headers)

	return response

def download_log_file_API(access_token,fileid,url = download_log_file_stem() ):
	return core_download_log_file(access_token,url)

def core_download_log_file(access_token,url):

	headers = headers_download_calAPI(access_token,access_token)

	payload = download_log_file_payload(fileid)

	response = get(url, json=payload, headers=headers)

	return response
