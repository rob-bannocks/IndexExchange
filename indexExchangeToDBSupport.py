# index-exchange-to-dbupport.py
#
# these are the main 2 functions called by index-exchange-to-db.py
from report_to_db_table_mapping import report_2_db_table_mapping # now param do we need this
from reportmanagementSupport import upload_existing_report, run_adhoc_report_to_download
from reportdownloadSupport import get_list_avaliable_fileIDs
from reportdownloadSupport import get_a_report_run_or_null
from utility import report_run_to_csv, return_time_now_str
from readwrite import write_list_to_csv_file
from authenticationSupport import return_auth_token_from_auth_struct,renew_auth_structure
from reportmanagementSupport import update_existing_report
from local_dbs import return_publisherid_db

def return_publishers_dict():
	return return_publisherid_db()

def return_publishers_list(dict=return_publishers_dict()):
	# convert to integer list
	list = [ int(key) for key in dict ]
	return list

def upload_and_run_reports_for_list(auth_struct,publishers_list_int,args,publishers_dict=return_publishers_dict(),verbose= False):
	"""
	This function implements the main functionality of fetching from the local store the command line
	named reports, uploading them to Index Exchange, running them and recording in the fileid_dict
	the fileID of the corresponging report for latter download (along with other important information
	needed for latter processing (i.e. the publisher_id for each fileID which in nowhere else recorded.
	"""
	# read in the reportIDs database
	#from local_json_dbs import read_ix_reportid_db,write_ix_reportid_db
	#reportIDs = read_ix_reportid_db()
	from shelve import open as shopen
	from local_shelve_dbs import return_ix_reportid_db
	reportIDs = return_ix_reportid_db()
	if verbose == True:
		print("type list ix db reportids ",type(reportIDs))
	# read in the reportIDs database
	auth_struct = renew_auth_structure(auth_struct)
	auth_token = return_auth_token_from_auth_struct(auth_struct)
	from reportmanagementSupport import get_list_int_active_reports
	list_reportids = get_list_int_active_reports(auth_token)
	if verbose == True:
		print("list active ids type : ",type(list_reportids))

	fileid_dict = {}
	for accountID in publishers_list_int:
		accountID_int = int(accountID)
		accountID_str = str(accountID)
		for ele in args:
			# renew auth_structure
			auth_struct = renew_auth_structure(auth_struct)
			auth_token = return_auth_token_from_auth_struct(auth_struct)

			# if we have record of an existant reportID for this publisher and report update that otherwise create new.
			update_report = False
			if accountID_str in reportIDs:
				if ele in reportIDs[accountID_str]:
					if 'reportID' in reportIDs[accountID_str][ele]:
						if verbose == True:
							print("found report id for publisher, ",accountID_str," report ",ele," with reportID, ",reportIDs[accountID_str][ele]['reportID'])
						# finally this has to be in the list of reportIDs
						potential_reportid = reportIDs[accountID_str][ele]['reportID']
						if verbose == True:
							print("type of potential_reportid is ",type(potential_reportid))
							print("type of list_reportids is ",type(list_reportids))
						# deal with database polution or sential values
						#if potential_reportid != None and potential_reportid != "0":
						try:
							potential_reportid = int(potential_reportid)
							if verbose == True:
								if potential_reportid in list_reportids:
									print("[int] reportid ",potential_reportid, " is in reportIDs")
								else:
									print("[int] reportid ",potential_reportid, " is NOT IN reportIDs")
							if potential_reportid in list_reportids:
								update_report = True
								update_reportid = int(potential_reportid)
								if verbose == True:
									print("Found reportID, ",potential_reportid," in list of reportIDS so will modify this")
							else:
								print("NOT Found reportID, ",potential_reportid," in list of reportIDS so will create new report.  Publisher ",accountID_str," report ",ele)
							if verbose == True:
								print("summary report list ",list_reportids[0:10])
						except:
							print("null or zero value found in reportID DB for report ",ele,"account", accountID_str," teating as non existant")
			
			# sometimes a reportID is returned by the list_acitve report API call when it is maked for deleton an cannot be updated.
			# if this happend we delete the report and create a new one
			replace_report = False
			if update_report == True:
				# update report
				result=update_existing_report(auth_token,[ accountID_int ],update_reportid,ele,fileType="csv",stop_on_error=False)
				if result == None:
					continue
				#reportIDs[accountID_str][ele]['createdX'] = return_time_now_str()
				result_report_int = update_reportid
				#reportIDs[accountID_str][ele]['last_updatedX'] = return_time_now_str()
				new_entry = reportIDs[accountID_str]
				new_subentry = new_entry[ele]
				new_subentry['last_updated'] = return_time_now_str()
				new_entry[ele] = new_subentry
				reportIDs[accountID_str] = new_entry
				
			if update_report == False:
				result_report_int = upload_existing_report(auth_token,[ accountID_int ],ele,fileType="csv",stop_on_error=False)
				if result_report_int == None:
					continue
				#reportIDs[accountID_str][ele]['createdX'] = return_time_now_str()
				new_entry = reportIDs[accountID_str]
				new_entry[ele] = { 'reportID' : result_report_int }
				new_entry[ele]['created'] = return_time_now_str()
				reportIDs[accountID_str] = new_entry
			
			# creation dater
			fileid_int = run_adhoc_report_to_download(auth_token,result_report_int)

			fileid_dict[ fileid_int ] = { 'publisher' : publishers_dict[ accountID_int ], 'report': ele , 'accountID' : accountID_int , 'status' : False, 'file_status': False, 'db_status': False, 'reportID': result_report_int }

	reportIDs.close()
	return fileid_dict,auth_struct

def fetch_report_runs(fileid_dict,auth_struct,write_to_database=True,write_to_file=False):
	reports_to_download = [ *fileid_dict ]

	# renew auth_structure
	auth_struct = renew_auth_structure(auth_struct)
	auth_token = return_auth_token_from_auth_struct(auth_struct)

	# list_int = sorted(get_list_avaliable_fileIDs(auth_token,status="new"))
	list_int = sorted(get_list_avaliable_fileIDs(auth_token))

	if len(list_int) == 0:
		return {}

	# if we will talk to the DB set up connection
	if write_to_database == True:
		from mysql_db import get_mysql_connection,close_connection,insert_or_update_db_row
		from mysql_db import csv_list_to_db_row
		from mysql_db import insert_csv_list_to_db
		from mysql_db import get_mysql_db_name
		database = get_mysql_db_name()
		my_db_connection =  get_mysql_connection(database=database)
		if my_db_connection == None:
			print("Error cannot connect to database")
			quit(1)
		cursor = my_db_connection.cursor()

	for id in fileid_dict:
		id_int = int(id)
		if fileid_dict[id]['status'] == False:

			# renew auth_structure
			auth_struct = renew_auth_structure(auth_struct)
			auth_token = return_auth_token_from_auth_struct(auth_struct)

			if id_int in list_int:

				result = get_a_report_run_or_null(auth_token, fileID=id_int,stop_on_error=False)
				if result == None:
					# ADD PUBLISHER AND REPORT ID AND DATE TO SPOOL TO RUN AGAIN
				elif result.status_code == 500:
					# this is server side error so leave file to be picked up next run
				elif result.status_code != 200:
					pass
				else:
					csv = report_run_to_csv(result.content.decode(),publisher_int=fileid_dict[id]['accountID'])

					# write out file or upload to database
					written_to_file=False
					written_to_database=False
	
					if write_to_file == True:
						# generate unique filename - use fileID
						write_list_to_csv_file(str(id),csv)
						fileid_dict[id]['file_status'] = True
						written_to_file=True
					else:
					if write_to_database == True:
						db_table = report_2_db_table_mapping[ fileid_dict[id]['report'] ]['db_table']
						if len(csv) != 1:
							insert_csv_list_to_db(cursor,db_table,csv)
							my_db_connection.commit()
						fileid_dict[id]['db_status'] = True
						written_to_database=True
	
					# update tuple
					# set status
					status = not ( write_to_file and not written_to_file ) and not (write_to_database and not written_to_database )
					if status == True:
						fileid_dict[id]['status']=True
		else:
		# del fileid_dict[id]
		# write the remianing_reports to storage
		
	if write_to_database == True:
		my_db_connection.commit()
		close_connection(my_db_connection)

	new_fileid_dict = {}
	for id in fileid_dict:
		st = fileid_dict[id]['status']
		if st == False:
			new_fileid_dict[id] = fileid_dict[id]
	return new_fileid_dict,auth_struct
