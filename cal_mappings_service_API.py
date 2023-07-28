# mappings_service_API.py
#

from calcoreAPI import headers_calAPI,calcoreget_no_payload
from urlencoding import string_to_urlstring

def buyer_mapping_API(auth_token,api_token=None, url = "https://app.indexexchange.com/api/cal/v1/mappings/buyers"):
	return calcoreget_no_payload(auth_token,url,api_token)

def campaign_mapping_API(auth_token,api_token=None, url = "https://app.indexexchange.com/api/cal/v1/mappings/campaigns"):
	return calcoreget_no_payload(auth_token,url,api_token)

def deal_mapping_API(auth_token,api_token=None, url = "https://app.indexexchange.com/api/cal/v1/mappings/deals"):
	return calcoreget_no_payload(auth_token,url,api_token)

def dsp_mapping_API(auth_token,api_token=None,url = "https://app.indexexchange.com/api/cal/v1/mappings/dsps"):
	return calcoreget_no_payload(auth_token,url,api_token)

def site_mapping_API(auth_token,api_token=None,url = "https://app.indexexchange.com/api/cal/v1/mappings/sites"):
	return calcoreget_no_payload(auth_token,url,api_token)

def partner_mapping_API(auth_token,api_token=None,url = "https://app.indexexchange.com/api/cal/v1/mappings/partners"):
	return calcoreget_no_payload(auth_token,url,api_token)

def generic_mapping_API(auth_token,mapping_name,api_token=None,urlbase = "https://app.indexexchange.com/api/cal/v1/mappings/"):
	url += string_to_urlstring(str(mapping_name)+"s")

	return calcoreget_no_payload(auth_token,url,api_token)

def old_buyer_mapping():
	from requests import get
	headers = headers_calAPI(auth_token,api_token)

	response = get(url, headers=headers)
	
	return response
