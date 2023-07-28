# cal_authenticationAPI.py

# functions to authentcate for cal

from settings import get_cal_api_key
from requests import post
from json import loads
from datetime import datetime,timedelta

def get_cal_auth_headers(apikey):
	headers = {
		"Content-Type" : "application/x-www-form-urlencoded" ,
		"Authorization" : "Basic "+apikey,
	}
	
	return headers

def extract_auth_response_from_auth_struct(dict):
	return dict['auth_struct']

def cal_auth_extract_expires_in_from_cal_auth_struct(dict):
	print(dict)
	return dict['auth_struct']['expires_in']

def cal_auth_extract_token_type_from_cal_auth_struct(dict):
	return dict['auth_struct']['token_type']

def cal_auth_extract_scope_from_cal_auth_struct(dict):
	return dict['auth_struct']['scope']

def cal_auth_extract_auth_token_from_cal_auth_struct(dict):
	return dict['auth_struct']['access_token']

def cal_auth_extract_expires_in_from_cal_auth_response(dict):
	return dict['expires_in']

def cal_auth_extract_token_type_from_cal_auth_response(dict):
	return dict['token_type']

def cal_auth_extract_scope_from_cal_auth_response(dict):
	return dict['scope']

def cal_auth_extract_auth_token_from_cal_auth_response(dict):
	return dict['access_token']

def get_cal_auth_url():
	return "https://identity.indexexchange.com/auth/realms/eventlog/protocol/openid-connect/token"

def get_cal_auth_payload():
	post_data = {
		"grant_type" : "client_credentials"
	}

	return post_data

def api_cal_auth_openid(apikey,url=get_cal_auth_url(),headers=None,payload=get_cal_auth_payload()):
	if headers == None:
		headers = get_cal_auth_headers(apikey)

	response = post(url, headers=headers, data=payload)
	
	return response

def cal_auth_response_to_cal_auth_struct(dict,issue_time,url,headers,payload,pricessing_fraction = 0.05):
	# proportion of token's life time remaining when its time to renew (includes buffer)
	expires_in = cal_auth_extract_expires_in_from_cal_auth_response(dict)
	delta_time_int= int( expires_in )
	# the expiry time should give time to renew not be the very last second!
	expiry_delta_time = int( delta_time_int * ( 1- pricessing_fraction ))
	expiry_time = issue_time + timedelta(seconds  = expiry_delta_time )
	#dict['expiry_time'] = expiry_time

	auth_struct = { "issue_time": issue_time,
			"auth_struct" : dict,
			"expiry_time" : expiry_time,
			"url" : url,
			"headers" : headers,
			"payload" : payload,
	}
	
	return auth_struct
	
def get_cal_auth_structure(apikey = get_cal_api_key(),url=get_cal_auth_url(),headers=None,payload=get_cal_auth_payload()):
	if headers == None:
		headers = get_cal_auth_headers(apikey)

	response = api_cal_auth_openid(apikey,url=url,headers=headers, payload=payload)
	
	if response.status_code != 200:
		print("auth failure")
		quit(1)

	issue_time = datetime.now()

	ret_dict = cal_auth_response_to_cal_auth_struct(loads(response.content.decode()),issue_time,url,headers,payload)

	return ret_dict

def renew_cal_auth_structure(auth_struct):
	current_time = datetime.now()
	if current_time > auth_struct['expiry_time'] :
		# new ticket
		return get_cal_auth_structure(url = auth_struct['url'],headers=auth_struct['headers'],payload=auth_struct['payload'])
	else:
		return auth_struct	
	
def dict_print(item):
	for i in item:
		print(i+":\t"+str(item[i]))
