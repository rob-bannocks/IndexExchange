# cal_download.py

from json import loads,dumps

# iterate through log files

from re import search as research
def url_to_fileid(url):
	reexp = r"(^https://app.indexexchange.com/api/cal/v1/files/)([1-9][0-9]*)$"
	fileid = research(reexp,url)

	return int(fileid.group(2))

def cal_api_response_to_dict(response,sub_dict=None):
	data = response.content.decode()

	if sub_dict != None:
		data_dict = loads(data)[sub_dict]

	return data_dict
