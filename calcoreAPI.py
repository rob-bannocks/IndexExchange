# calcoreAPI.py
#
# API functions to interact with the Log retrieval CAL API at Index Exchange
#

from requests import get

def headers_calAPI(auth_token,api_token=None):
	headers = {
		"accept": "application/json",
		"Authorization": "Bearer "+auth_token
	}

	if api_token != None:
		headers['access_token'] = api_token

	return headers

def calcoreget_no_payload(auth_token,url,api_token=None):
	headers = headers_calAPI(auth_token,api_token)

	response = get(url, headers=headers)
	
	return response

if __name__ == "__main__":
	print("CAL API core tests")
