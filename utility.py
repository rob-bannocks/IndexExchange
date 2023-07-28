# utility functions
from settings import getEmail
from re import sub
from datetime import datetime

def list_ints_to_string(list,sepperator=","):
    return sepperator.join([str(i) for i in list])

def return_time_now_str():
	#return return_time_now.strftime("%A %d %B %Y %I-%M-%S %p %Z")
	now_time = return_time_now()
	return now_time.strftime("%A %d %B %Y %I-%M-%S %p %Z")

def return_time_now():
	return datetime.now()

def return_unique_report_name_stem():
	return "API Tempoary AutoUploaded report by "

def generate_unique_report_name():
	#import datetime
	#now = datetime.datetime.now()
	now = datetime.now()
	email = IndexExchangeReportTitleString(getEmail())
	date_suffix = now.strftime("%A %d %B %Y %I-%M-%S %p %Z")
	unique_report_name_stem = return_unique_report_name_stem()
	unique_report_name = unique_report_name_stem +email+" " + date_suffix
	return unique_report_name

def IndexExchangeReportTitleString(str):
	# can only contain alphanumeric characters with spaces, hyphens, underscores, and periods
	str = str.replace("@", " at ")
	return sub(r'^[a-zA-Z]- _\.',"_",str)

def text_to_csv(text):
	from csv import reader
	csv = reader(text.strip().splitlines())
	csv_array = [ i for i in csv ]
	# return_csv = [ {heading[i]: csv[i,j] for i in range(0,length(heading)) } for j in csv ]
	return csv_array

def report_run_to_csv(text,publisher_int=0):
	csv=text_to_csv(text)
	if len(csv) == 0:
		print("Error sent null csv text length is ",len(csv),"csv is : ",csv)
		quit(1)
	[ csv[i].insert(0, publisher_int) for i in range(1,len(csv)) ]
	csv[0].insert(0, 'publisher_id')
	
	return csv

def clense_ints(int_feilds,csv,sentinel_value="-9999"):
	header = csv[0]
	for item in int_feilds:
		headings = csv[0]
		if headings.count(item)==1:
			index = header.index(item)
			for loc in range(1,len(csv)):
				try:
					throw_away = int(csv[loc][index])
				except:
					csv[loc][index] = sentinel_value
	return csv
