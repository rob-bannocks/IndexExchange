# exchangeratesAPI.py
#

from requests import get
from calcoreAPI import headers_calAPI,calcoreget_no_payload
from urlencoding import string_to_urlstring

def exchange_rates_API(auth_token, base_url = "https://app.indexexchange.com/api/cal/v1/exchange-rates", date=None, currency=None):

	if date != None or currency != None:
		ampersand=False
		base_url += "?"
		if date != None:
		        base_url += "date="+string_to_urlstring(date)
		        ampersand = True
		if currency != None:
		        if ampersand == True:
		                base_url += "&"
		        base_url += "currency="+string_to_urlstring(currency)
	
	url = base_url

	return calcoreget_no_payload(auth_token,url)
