# authenticatationAPI.py
#
# contains raw authentication API calls
#

from requests import post
from requests.exceptions import RequestException
from json import loads

def indexExchangeURL():
	"""
	This function sets the URL for login for Index Exchange and returns this.  This 
        therefore is a central place to store the URL.
	Returns:
 		
    """
	url = "https://app.indexexchange.com/api/authentication/v1/login"
	return url

def indexExchangeHeaders():
	"""
	Set the headers need to authenticate to IndexExchange.  Takes no input
	Returns:
		a structure of headers to use with api_generate_user_account_token
	"""
	headers = {
		"accept": "application/json",
		"content-type": "application/json"
	}
	
	return headers

def api_generate_user_account_token(payload,url=indexExchangeURL(),headers = indexExchangeHeaders()):
	try:
		response = post(url=url, headers=headers,json=payload)
	except RequestException as e:  # This is the correct syntax
	#except requests.exceptions.RequestException as e:  # This is the correct syntax
		raise SystemExit(e)

	if response.status_code != 200 :
		raise SystemExit("[api_generate_user_account_token] Authentication failed",response.status_code)

	return response.json()

def return_refresh_token_payload(refresh_token):
	payload = {
		"refreshToken": refresh_token
	}
	
	return payload

def return_refresh_token_headers():
	headers = {
		"accept": "application/json",
		"content-type": "application/json"
	}

	return headers

def return_refresh_token_url():
	return "https://app.indexexchange.com/api/authentication/v1/refresh"

def api_refresh_token(refresh_token,url = return_refresh_token_url(), headers = return_refresh_token_headers(), payload = None):
	"""

	"""
	if payload == None:
		payload = return_refresh_token_payload(refresh_token)

	response = post(url,headers=headers,json=payload)
	
	if response.status_code != 200:
		print("Error response code ",response.status_code, " returned")
		quit(1)

	response_dict = loads(response.content.decode())
	
	return response_dict
