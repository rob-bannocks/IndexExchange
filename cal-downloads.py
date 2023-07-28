# cal-download.py

from cal_authenticationAPI import get_cal_auth_structure
from cal_authenticationAPI import cal_auth_extract_auth_token_from_cal_auth_struct
from cal_log_retrieval_API import impression_event_logs_API,download_log_file_via_url_API,bid_event_logs_API
from json import loads,dumps
from gzip import decompress
from utility import text_to_csv, report_run_to_csv
from utility import clense_ints
from cal_utility import cal_api_response_to_dict
from cal_log_retrieval_API import download_log_file_stem
from mysql_db import get_mysql_connection, close_connection,insert_or_update_db_row_cursor
from cal_utility import  url_to_fileid
from cal_mappings_service_API import *
from mysql_db import insert_csv_list_to_db
from local_dbs import return_publisherid_db
from cal_settings import return_apikey_table_with_cursor,update_download_log_table_entry
from cal_authenticationSupport_API import get_auth_structure_from_publisher_id
from cal_settings import get_cal_download_log_table_by_api_with_cursor, get_cal_data_table_by_api_with_cursor, return_download_log_table_as_publisher_id_list
from cal_settings import return_int_feilds_from_table_definition,return_table_feilds_with_cursor

def data_list_transform_null(list,publisher_id=0):
	return list

def add_publisher_id_to_item(item,publisher_id):
	item['publisher_id'] = publisher_id
	return item

def dict_replace_key_value(dict,publisher_id,key,value):
	dict[key] = value
	return dict

def data_list_transform_campaign_mapping(list,publisher_id=0):
	print(loads(list,indent=8))
	# Deal with the creatives
	# assemble union list
	# write to table
	# for now
	list = [ dict_replace_key_value(item,'creatives',str( [ item[creative_id] for creative_id in item[creative_id ] ] )) for item in dict ] 
	# return the standard table	
	new_list = [ add_publisher_id_to_item(item,publisher_id) for item in list ]
	return new_list

def data_list_transform_buyer_mapping(list,publisher_id=0):
	new_list = []
	for item in list:
		# flatten section_id
		item['section_id'] = ",".join([ str(entry) for entry in item['section_id'] ] )
		# add publisher_id
		item['publisher_id'] = publisher_id
		new_list.append(item)
	return new_list

def data_list_transform_impression_events(list,publisher_id):
	# Get current list of downloads
	# we only use some of the informaion from this API call.  This is then
	# used to fetch the files, and store them sepperate from this process.
	new_list = [item.update({'publisher_id':str(publisher_id)}) for item in list ]
	if debug == True:
		print("list after addition of publisher_id",list)
	selection = ( 'hour','downloadURL','md5sum','downloadStatus','dateCreated'  )
	if debug == True:
		print(list[0])
	new_list = [ {key : item[key] for key in selection} for item in list ]
	if debug == True:
		print("list after selection of columns ", selection,":",new_list)
	
	return new_list

def data_list_transform_bid(list,publisher_id):
	# fltten
	return_list = []
	for item in list:
		if 'parts' in item:
			subitem=item['parts']
			for item2 in subitem:
				new_item = item.copy()
				del new_item['parts']
				new_item.update(item2)
				return_list.append(new_item)
				if debug == True:
					print("return_list",return_list)
		else:
			return_list.append(item)
	selection = ( 'hour','downloadURL','md5sum','downloadStatus','dateCreated' )
	if debug == True:
		print(return_list[0])
	new_list = [ {key : item[key] for key in selection} for item in return_list ]
	if debug == True:
		print("List after selection of columns ", selection,":",new_list)
	
	return new_list


# Need to put publisher in impressions, bids, deals,site, campaign, both in table definnitions and functions calls.
#
#

def do_main_old(debug=False):
	apikey_list = return_apikey_table_with_cursor(cursor)
	if debug == True:
		print(apikey_list)
	do_first = True
	for item in apikey_list:
		auth_struct = get_cal_auth_structure(apikey_list)
		auth_token = cal_auth_extract_auth_token_from_cal_auth_struct(auth_struct)
		if debug == True:
			print("doing item: ",item)
			print("auth: ",auth_struct)
			print("publisher_id",apikey_dict['publisher_id'])
		for entry in download_dict:
			print("doing",entry)
		if do_first == True:
			do_first = False
			
		
#
# call the mapping
#
def do_mapping_downloads(downloads_dict,publisher_id):
# not really "mapping" also includes logs and potentially exchange rates too.
# so change the name of the function.
#
	pass

def do_log_service(download_dict):
	my_db_connection = get_mysql_connection()
	if my_db_connection == None:
		print("Error connecting to data base")
		sysExit(1)
	cursor = my_db_connection.cursor()
	publisher_dict = return_apikey_table_with_cursor(cursor)
	downloaded_files = return_download_log_table_as_publisher_id_list(cursor)
	for publisher_id,apikey in publisher_dict:
		if debug == True:
			print("publisher_id:",publisher_id,"apikey:",apikey)
		if publisher_id == 0:
			continue
		auth_struct = get_cal_auth_structure(apikey)
		auth_token = cal_auth_extract_auth_token_from_cal_auth_struct(auth_struct)
		for download_dict_item in download_dict:
			value = download_dict[download_dict_item]
			dict = process_download_table(auth_token,download_dict_item,value,publisher_id)
			if dict != {} :
				for entry in dict:
					if 'downloadURL' in entry:
						# if id in db check status download if new
						# if id not in db download
						url = entry['downloadURL']	
						# get fileid from url
						fileid = str(url_to_fileid(url))

						if 'downloadStatus' in entry:
							download_status = entry['downloadStatus']
						else:
							download_status = "updated"

						if debug == True:
							print("="*120)
							print("type of downloaded_files",type(downloaded_files))
							print("fileid of ",type(fileid))
							print("to download ",entry['downloadURL'])
							print("entry : ",entry)
							print("fileid,",fileid,"is", fileid in downloaded_files)
							print("Logic:", ( fileid not in downloaded_files ) or ( fileid in downloaded_files and download_status == "updated" ) )
							print("Logic breakdown: fileid not in downloaded_files ",  fileid not in downloaded_files )
							print("Logic breakdown: fileid in downloaded_files and download_status == \"updated\"", fileid in downloaded_files and download_status == "updated" )
							print(entry)
							print(downloaded_files)
							# print("Logic breakdown:", ( fileid not in downloaded_files ) or ( fileid in downloaded_files and download_status == "updated" ) )

						if ( fileid not in downloaded_files ) or ( fileid in downloaded_files and download_status == "updated" ):
	
							response = download_log_file_via_url_API(auth_token,url)
						
							content = response.content
							decompressed = decompress(content)
							decoded = decompressed.decode()
							if debug == True:
								print("--------------------------------------------------")
								print(response.status_code)
								if debug == True:
									print( decoded )
						
							# csv = text_to_csv(decoded)
							
							# add in publisher_id
							csv = report_run_to_csv(decoded,int(publisher_id))
							if len(csv) > 1:
								
								table_name = get_cal_data_table_by_api_with_cursor(cursor,download_dict_item)
								if debug==True:
									print("looking up ",download_dict_item," in db gives table_name",table_name)
	
								# get list of columns from table definition
								
								# get int feilds
								int_feilds = return_int_feilds_from_table_definition(cursor,table_name, exclude_list=[ "publisher_id" ])
	
								# clense data ensuring all int feilds are send ints
								csv = clense_ints(int_feilds,csv)
								if debug == True:
									print("CSV1:",csv)
	
								# add other column
								[ item.append('other') for item in csv ]
	
								# drop feilds that are not in the table definition
								db_feilds = return_table_feilds_with_cursor(cursor,table_name)
								db_feilds.append("publisher_id")
								if debug == True:
									print("db_feilds",db_feilds)
	
								# move none present feilds to "other feild"
								headings = csv[0]
								if debug == True:
									print("Headings",headings)
								for item in headings:
									if item not in db_feilds:
										# add to other
										if headings.count(item)>1 :
											print("duplicate heading",item,"found bailing out")
											quit(1)
										
										index = headings.index(item)
										# delete from header
										if debug == True:	
											print("Removing",item,"from csv as not in table definition")
										# delete feilds
										csv_other = [ element[index] for element in csv.copy() ]
										csv_sql = [ element.pop(index) for element in csv ]
										new_csv = []
										other_heading = 'other'
										if other_heading in headings:
											other_index = headings.index(other_heading)
											if debug == True:
												print("CSV other:",csv_other)
												print("CSV sql:",csv)
	
											for idx in range(1,len(csv)):
												if debug == True:
													print(type(csv))
													print(type(csv_sql))
													print(type(csv_other))
													print(type(csv_other[index]))
													print(type(csv[idx]))
													#print(type(csv[idx][other_heading]))
													print(csv_other)
													print(csv[idx][other_index])
													print(csv[idx][other_index])
													print( str( csv[idx][other_index] ))
													print( " item="+str(csv_other[idx]) )
												csv[idx][other_index] = str( csv[idx][other_index] )+" "+item+ "="+str(csv_other[idx])
								if debug == True:
									print("CSVF:",csv)
	
								# write to db
								if table_name == None :
									print("Error ",download_dict_item," not in API to db table table")
									quit(1)
								if debug == True:
									print("download_dict_item ",item," table ",table_name)
		
								insert_csv_list_to_db(cursor,table_name,csv)
								# commit
								my_db_connection.commit()
							else:
								if debug == True:
									print("Error sent null or just headers with CSV")
							# record in download log
							# 
							# isert entry into cal_download_log
							if debug == True:
								print(entry)
							hour = entry['hour']
							origin = download_dict_item
							
							update_download_log_table_entry(cursor, hour, url, publisher_id, origin)
							my_db_connection.commit()
						else:
							if debug == True:
								print("skipping ",publisher_id,"as in download table")
					else:
						print("Item in list from",download_dict_item,"without a download URL",entry)
			if debug == True:
				print(dict)
				print("+"*85)
	cursor.close()
	close_connection(my_db_connection)

def do_downloads_mappings_service(download_dict):
	my_db_connection = get_mysql_connection()
	if my_db_connection == None:
		print("Error connecting to data base")
		sysExit(1)
	cursor = my_db_connection.cursor()
	publisher_dict = return_apikey_table_with_cursor(cursor)
	done_once = False
	for publisher_id,apikey in publisher_dict:
		if debug == True:
			print("publisher_id:",publisher_id,"apikey:",apikey)
		if publisher_id == 0:
			continue
		auth_struct = get_cal_auth_structure(apikey)
		auth_token = cal_auth_extract_auth_token_from_cal_auth_struct(auth_struct)
		for item in download_dict:
			value = download_dict[item]
			if debug == True:
				print("item:",value)
			if ( value['flag'] == 'C' and done_once == False ) or value['flag'] == 'P':
				if done_once == False:
					done_once = True
				dict = process_download_table(auth_token,item,value,publisher_id)
				if dict != {} :
					csv = dict_to_csv(dict)
					table_name = get_cal_data_table_by_api_with_cursor(cursor,item)
					if table_name == None :
						print("Error ",item," not in API to db table table")
						quit(1)
					if debug == True:
						print("item ",item," table ",table_name)
					insert_csv_list_to_db(cursor,table_name,csv)
					my_db_connection.commit()
					if debug == True:
						print("-"*80)
					#my_db_connection.commit()
			else:
				if debug == True:
					print("Skipping ",item," as already done and flag is ",value['flag'])
	cursor.close()
	close_connection(my_db_connection)

def process_download_table(auth_token,key,value,publisher_id):
			if debug == True:
				print("doing item:", key)
				print("doing item value:", value)
			response = value['function'](auth_token)
			#response = downloads_dict[key]['function'](auth_token)
			response_text = response.content.decode()
			if response.status_code != 200:
				print("Response code for mapping download",key,"returns status code",response.status_code,":",loads(response.content.decode())['message'],"for publisher_id",publisher_id)
				if debug == True:
					print("-"*80)
				#continue
				return {}
			if debug == True:
				print(dumps(loads(response_text)))
			data_dict = cal_api_response_to_dict(response,value['sub_dict'])
			data_dict = value['transform'](data_dict,publisher_id)

			return data_dict

def dict_to_csv(dict):
			cols = dict[0].keys()
			if debug == True:
				print("cols : ",cols)
			array = [ [ str(item[col]) for col in cols ] for item in dict ]
			array.insert(0,cols)
			if debug == True:
				print(array)
			return array

def do_old():
	my_db_connection = get_mysql_connection()
	if my_db_connection == None:
		print("Error connecting to data base")
	cursor = my_db_connection.cursor()

	publisher_dict = return_apikey_table_with_cursor(cursor)

	apikey = publisher_dict[1][1]
	auth_struct = get_cal_auth_structure(apikey)
	auth_token = cal_auth_extract_auth_token_from_cal_auth_struct(auth_struct)

	cursor.close()
	close_connection(my_db_connection)

	# get logs
	# cal_auth_extract_auth_token_from_cal_auth_struct(auth_struct)	
	reply = impression_event_logs_API(auth_token)
	list_json = reply.content.decode()
	list_dict = loads(list_json)
	avaliable_downloads = list_dict['availableDownloads']

	url = avaliable_downloads[0]['downloadURL']
	# download_log_fileAPI( url=url)
	list_one_dict = avaliable_downloads[0]
	url = list_one_dict['downloadURL']
	response = download_log_file_via_url_API(auth_token,url)
	
	if debug == True:
		print("--------------------------------------------------")
		print(response.status_code)
	content = response.content
	if debug == True:
		print(content)
	decompressed = decompress(content)
	decoded = decompressed.decode()
	debug = True
	print(dumps(avaliable_downloads,indent=8))
	for entry in avaliable_downloads:
		fileid=url_to_fileid(entry['downloadURL'])
	dict = { url_to_fileid(entry['downloadURL']):entry for entry in avaliable_downloads }
	csv = text_to_csv(decoded)
	len_array = len(csv[0])
	for item in csv:
		if len(item) != len_array:
			print(item)
	
	fileid = url_to_fileid(url)
	print(fileid)
	print(url)

def do_old_db():
	my_db_connection = get_mysql_connection()  # BD now defaults!
	# , close_connection,insert_or_update_db_row_cursor
	if my_db_connection == None:
		print("Error connecting to data base")
	cursor = my_db_connection.cursor()

	from cal_settings import get_cal_download_log_table_by_api_with_cursor, get_cal_data_table_by_api_with_cursor
	download_table = get_cal_download_log_table_by_api_with_cursor(cursor,"impression_events")
	data_table = get_cal_data_table_by_api_with_cursor(cursor,"impression_events")
	# upp load data to db, add entruy for file id
	print("download table ",download_table, " data table ", data_table)
	print("+"*80)
	cursor.close()
	close_connection(my_db_connection)

	for item in dict:
		print(item,":",dict[item]['downloadURL'])
	publisher_ids =  return_publisherid_db()
	print(dumps(publisher_ids,indent=8))
#if __name__ == "__main__":
import sys
import getopt

# defaults
do_bid = False
do_impression = False
do_mappings=True

debug = False


def usage():
	print(sys.argv[0]+" [-h] | [-D] [-M] [-i] [-b] [-l]")
	print("options:")
	print("	-M - skip mapping tables")
	print("	-b - do bid log table")
	print("	-i - do cal download log table")
	print("	-l - both -l and -b")
	print("	-D - run in debug mode (output is very volimious)")
	print()
	print("	-h print this help information")
try:
	opts, args = getopt.getopt(sys.argv[1:], "hMDlib")
except getopt.GetoptError as err:
	# print help information and exit:
	print(err)  # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
	output = None
for o, a in opts:
	if o == "-D":
		debug = True
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-i"):
		do_impression = True
	elif o in ("-b"):
		do_bid = True
	elif o in ("-l"):
		do_bid = True
		do_impression = True
	elif o in ("-M"):
		do_mappings = False
	else:
		assert False, "unhandled option"

	# iterate through log files
downloads_mapping_service = { # API name : { flag : P - do all mapping tables, C - only do the table for first entry in apikey table function: API function to fetch REST data : transform: function to transform
	"buyer_mapping"	: { "flag" : "C" , "sub_dict" : "data", "function" : buyer_mapping_API , 'transform' : data_list_transform_null },
	"campaign_mapping": { "flag" : "P" , "sub_dict" : "data", "function" : campaign_mapping_API , 'transform' : data_list_transform_campaign_mapping },
	"deal_mapping"	: { "flag" : "P" , "sub_dict" : "data", "function" : deal_mapping_API , 'transform' : data_list_transform_buyer_mapping },
	"dsp_mapping"	: { "flag" : "C" , "sub_dict" : "data", "function" : dsp_mapping_API , 'transform' : data_list_transform_null },
		"site_mapping"	: { "flag" : "P" , "sub_dict" : "data", "function" : site_mapping_API , 'transform' : data_list_transform_null },
		"partner_mapping": { "flag" : "C" , "sub_dict" : "data", "function" : partner_mapping_API , 'transform' : data_list_transform_null },
		#"exchange_rates": { "flag" : "C" , "sub_dict" : "data", "function" : exchange_rates_API , 'transform' : data_list_transform_null },
}
	
downloads_mappings_once = { # API name : { frequency : H - hourly or D - daily flag: A - all publisher_ids or F - first only, function: API function to fetch REST data : transform: function to transform
	"buyer_mapping"	: { "flag" : "C" , "sub_dict" : "data", "function" : buyer_mapping_API , 'transform' : data_list_transform_null },
	"dsp_mapping"	: { "flag" : "C" , "sub_dict" : "data", "function" : dsp_mapping_API , 'transform' : data_list_transform_null },
	"partner_mapping": { "flag" : "C" , "sub_dict" : "data", "function" : partner_mapping_API , 'transform' : data_list_transform_null },
}

downloads_log_service = { # flat is ignored for this service
	"impression_events" : { "flag" : "P" , "sub_dict" : "availableDownloads" , "function" : impression_event_logs_API, 'transform' : data_list_transform_null },
	"bid_events" 	: { "flag" : "P" , "sub_dict" : "availableDownloads" ,"function" : bid_event_logs_API , 'transform' : data_list_transform_bid },
}

#downloads_log_service = {}
do_impression_and_bid =False
if  do_impression == False:
	del downloads_log_service['impression_events']

if  do_bid == False :
	del downloads_log_service[ 'bid_events' ] 

if  do_bid == True or do_impression == True:
	do_impression_and_bid = True

if debug == True:
	print("do_impression",do_impression)
	print("do_bid",do_bid)
	print("do_mappings",do_mappings)

if do_mappings == True:
	if debug == True:
		print("doing mappings with",downloads_mapping_service)
	do_downloads_mappings_service(downloads_mapping_service)

if do_impression or do_bid == True:
	if debug == True:
		print("doing logs with ",downloads_log_service)
	do_log_service(downloads_log_service)
