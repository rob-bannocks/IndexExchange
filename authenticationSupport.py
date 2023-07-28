# authenticationSupport.py
# This file contains functions support functions to wrap raw functions in authenticationAPI.py
# The main thrus is to get an authorisation token from Index Exchange
# it reads username (email address and password) with functions from settings.py
# it uses the standard requests library.
# 
# api_response, login_response, authResponse
#

from settings import getEmail, getPassword
from authenticationAPI import api_generate_user_account_token
from authenticationAPI import indexExchangeURL
from authenticationAPI import indexExchangeHeaders
from datetime import datetime,timedelta
from authenticationAPI import api_refresh_token

def indexExchangePayload( email=getEmail(), password=getPassword()):
	"""
	This function gets the username and password to use with the api_generate_user_account_token function.
	It uses the settings library/file and the functions getEmail and getPassword to construct
	a dict with username and password.  This can be passed to the api_generate_user_account_token function
	Returns:
		A payload structure
	"""
	
	payload = {
		"password": password,
  		"username": email
	}
	return payload
	
def get_auth_header(auth_token):
	"""

	"""
	returnval = {
		"accept": "application/octet-stream",
    		"Authorization": "Bearer "+str(auth_token)
	}

	return returnval

def get_auth_update_report_header(auth_token):
	header = get_auth_header(auth_token)	
	header['content-type'] = "application/json"
	
	returnval = {
		"content-type": "application/json",
		"accept": "application/octet-stream",
    		"Authorization": "Bearer "+str(auth_token)
	}

	return returnval
	return header 

def get_auth(payload=indexExchangePayload()):
	return api_generate_user_account_token(payload=payload)
	
def extract_auth_token_value(authResponse_dict):
	return authResponse_dict['access_token']
	
def get_auth_token():
	return extract_auth_token_from_login_response(get_auth())
	
def extract_authResponse_value(login_response_dict):
	return login_response_dict['authResponse']
	
def extract_login_response_value(api_response_dict):
	return api_response_dict['loginResponse']
	
def extract_auth_token_from_login_response(loginResponse):
	return extract_auth_token_value(extract_authResponse_value(extract_login_response_value(loginResponse)))
	
def return_token_time_proportion_remaining_fraction():
	return 0.1
	#return 0.99 # for testing

def return_authResponse_expiry_times(authResponse_dict,now, token_time_proportion_remaining_fraction = return_token_time_proportion_remaining_fraction()):
# proportion of token's life time remaining when renew
	expiry_time = extract_expires_in_value(authResponse_dict)
	delta_time_int= int( expiry_time )
	renew_delta_time = int( delta_time_int * (1 - token_time_proportion_remaining_fraction ) )
	renew_time = now + timedelta( seconds = renew_delta_time )
	# the expiry time should give time to renew not be the very last second!
	expiry_delta_time = int( delta_time_int * (1 - token_time_proportion_remaining_fraction **2) )
	expiry_time = now + timedelta(seconds  = expiry_delta_time )
	#expiry_time = now + timedelta(seconds  = delta_time_int )

	return renew_time, expiry_time

def return_expiry_times_auth_struct(auth_struct,issue_time,token_time_proportion_remaining_fraction = return_token_time_proportion_remaining_fraction()):
	return return_authResponse_expiry_times(auth_struct['auth'],issue_time, token_time_proportion_remaining_fraction = token_time_proportion_remaining_fraction )

def renew_auth_structure(auth_struct):
	current_time = datetime.now()
	if current_time > auth_struct['expiry'] :
		# new ticket
		return get_auth_structure(url = auth_struct['url'],headers=auth_struct['headers'],payload=auth_struct['payload'])

	elif current_time > auth_struct['renew_time']:
		# renew ticket
		issue_time = datetime.now()
		auth_struct['auth'] = api_refresh_token(auth_struct['auth']['refresh_token'])
		renew_time,expiry_time = return_expiry_times_auth_struct(auth_struct,issue_time)
		auth_struct['expiry'] = expiry_time
		auth_struct['renew_time'] = renew_time

		return auth_struct
	else:
		return auth_struct	

def get_auth_structure(url=indexExchangeURL(),headers=indexExchangeHeaders(),payload=indexExchangePayload()):
	"""
		This function gets an auth structure and wraps it in a structure with a time of issue and an expiry
	"""
	issue_time = datetime.now()
	api_response = api_generate_user_account_token(payload=payload)
	authResponse_dict = extract_authResponse_value(extract_login_response_value( api_response ) )

	expiry_time = extract_expires_in_value(authResponse_dict)
	delta_time = int( expiry_time )
	token_time_proportion_remaining_fraction = 0.1 # proportion of token's life time remaining when renew
	renew_delta_time = int( delta_time * (1 - token_time_proportion_remaining_fraction ) )
	renew_time = issue_time + timedelta( seconds = renew_delta_time )
	expiry_time = issue_time + timedelta(seconds  = delta_time )
	
	renew_time,expiry_time = return_authResponse_expiry_times(authResponse_dict,issue_time)
	auth_struct = {
		'issue_time' : issue_time,
		'auth' : authResponse_dict ,
		'expiry' : expiry_time,
		'renew_time': renew_time,
		'url' : url,
		'headers' : headers,
		'payload' : payload,
	}

	return auth_struct

def return_auth_token_from_auth_struct(auth_struct):
	return extract_auth_token_value(auth_struct['auth'])

def extract_expires_in_value(authResponse_dict):
	return authResponse_dict['expires_in']

def api_generate_service_account_token():
	"""
	This function gets an authentication structure for a service account.
	Parameters:
		Input: 
	"""
	# not yet implemented
	pass
	
if __name__ == "__main__":
	auth_struct = get_auth_structure()
	print(auth_struct)

def old():
	def extract_auth_token(auth_response):
		return auth_response['authResponse']
	
	if __name__ == "__main__":
		response2url=api_generate_user_account_token(url=indexExchangeURL(),headers=indexExchangeHeaders(),payload=indexExchangePayload() )
		#responseJson=response2url.json()
		print(response2url)
		print("===================================================")
		print("===================================================")
		print(extract_login_response_value(response2url))
		print("===================================================")
		print("===================================================")
		print(extract_authResponse_value(extract_login_response_value(response2url)))
		print("===================================================")
		print(extract_auth_token_value(extract_authResponse_value(extract_login_response_value(response2url))))
		print("===================================================")
		print(extract_auth_token(extract_authResponse_value(extract_login_response_value(response2url))))
		print("===================================================")
		print("email : ", getEmail())
		#print(response2url)
		print("===================================================")
		struct = get_auth_structure()
		print("===================================================")
		#print(struct)
		new_struct = renew_auth_structure(struct)
		print("===================================================")
		print(new_struct)
