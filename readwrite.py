# readwrite
# functions to read and write to files, usualy in json.
#

from settings import get_templates_store,get_data_download_store
import os
from json import dumps,load
import sys
from utility import generate_unique_report_name
from csv import writer

def save_report_run(fileID,dir=get_data_download_store(),stop_on_error=True):
    from reportdownloadAPI import api_download_a_report_file

    response =  api_download_a_report_file(get_auth_token,)
    if stop_on_error == False:
        return response # if error api_ will have stopped program flow in this case
    else:
        if response.status_code != 200:
         return None
        else:
         return response # which should be a decoded file
    file = api_download_a_report_file(auth_token,str(fileID))
    write_file = os.path.join(dir,str(fileID))
    with open(write_file, 'w') as file:
       file.write(file) # 

def save_specific_report_in_json(reportID,use_report_number=False,dir=get_templates_store(),verbose=False):
    from reportmanagementSupport import get_specific_report_in_json
    """
     This function takes a report reportID and downloads it and 
     stores this in the template store by report name unless
     user_report_number is True in which it saves the file in
     a file by its reportID number.  A reportID means the
     specification for a report (which is subsequently run)
    """
    reportjson = get_specific_report_in_json(reportID)
    report_json_indent = dumps(reportjson, indent = 1)
    if reportjson != None:
        if use_report_number == True:
            filename = str(reportID)
        else:
            filename = str(reportjson["reportDefinition"]["reportTitle"])
            # need to sanatise by removing any "/" characters
            filename = filename.replace("/",'')
        write_file = os.path.join(dir,filename)
        with open(write_file, 'w') as file:
            file.write(report_json_indent) # use `json.loads` to do the reverse
    else:
        SystemExit("Report fetch failed for report ",reportID)

def read_template_report_spec(report_name,store):
	read_file = os.path.join(store,str(report_name))
	assert os.path.isfile(read_file) and os.access(read_file, os.R_OK), \
       f"File {read_file} doesn't exist or isn't readable"
	with open(read_file) as loaded_file:
		report_json = load(loaded_file)
		return report_json

def get_report_from_local_store(report_name):
    return read_template_report_spec(report_name,store=get_templates_store())

def write_to_file(auth_token,fileID,filename,dir=get_data_download_store(),stop_on_error=True):
    from reportdownloadSupport import get_a_report_run
    response = get_a_report_run(auth_token,fileID,stop_on_error=stop_on_error)
    if stop_on_error == False:
        if response.status_code != 200:
           return None
        write_response = response.content
    else:
        write_response = response

    filename = filename.replace("/",'')
    write_file = os.path.join(dir,filename)
    try:
       with open(write_file, 'w') as file:
          file.write(write_response)
    except:
      return None

#
# simply avoid all the queues by having a tuple of (publisher,report via REport Name, Last run date)
def read_tuple(tuple_filepath):
    pass

# use pickle!
def write_tuple(tuple_filepath):
    pass

def write_list_to_csv_file(filename, list,dir=get_data_download_store()):
## check list is 2-d

    filepath = os.path.join(dir,filename)
    try:
       file = open(filepath,"w+",newline='')
    except:
       print("unable to open file ",filepath)
       quit(1)

    with file:
         write = writer(file)
         write.writerows(list)
