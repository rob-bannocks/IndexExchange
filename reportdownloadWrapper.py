# reportdownloadWrapper
#
# this file contains whole functions which implement an action, e.g. download a report
# doing all the work including obtaining authentication and calling other functions
from settings import get_data_download_store
def download_a_report_run_as_csv(fileid,stop_on_error=True):
	from authenticationSupport import get_auth_token
	from reportdownloadSupport import get_a_report_run_or_null
	from utility import text_to_csv,report_run_to_csv

	auth = get_auth_token()
	response = get_a_report_run_or_null(auth,fileid,stop_on_error=stop_on_error)

	# the next line is now done by the API call
	# text=response.content.decode()
	if stop_on_error == False:
		if response.status_code != 200:
			return None
		else:
			return response # with stop_on_error=False return raw response object
		
	csv = report_run_to_csv(response.decode())
	return csv
