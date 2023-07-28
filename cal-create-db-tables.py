#!python3

# create-db-tables.py
#
# script to set up and initially populate the tables needed for the scripts to run

# 1. The api to tables mapping table (prog_api_to_db_table), -a option
# 2. The log tables
# 3. the mappings service tables

import mysql.connector
from mysql_db import insert_or_update_db_row_cursor,insert_csv_list_to_db
from mysql_db import get_mysql_connection, select_column_with_cursor
from cal_settings import cal_api_to_db_table_mapping_table_name
from cal_settings import get_apikeys_table_name
import sys
import getopt

# defaults
do_api_tables = True
do_api_tables_data = True
do_mapping_tables = True
data_display = True

do_campaign_mapping = True
do_auth_table = True
do_impression_log = True
do_bid_log = True
do_cal_download_log = True
debug = False


def usage():
	print(sys.argv[0]+" [-h] | [-D] [-a] [-d] [-m] [-p] [-c] [-A] [-i] [-b] [-l]")
	print("options:")
	print("	-a create api table")
	print("	-d populate api table")
	print("	-m create mapping tables")
	print("	-p print contents of api mapping table")
	print("	-c create campaign tables")
	print("	-A create authentication table")
	print("	-i create impressions log table")
	print("	-b create bid log table")
	print("	-l create cal download log table")
	print("	-D run in debug mode")
	print()
	print("	-h print this help information")
try:
	opts, args = getopt.getopt(sys.argv[1:], "hDadlmpcAibl")
	options = [ item[0] for item in opts ]
	if ( len(sys.argv) > 1 and "-D" not in options )  or (  "-D" in options and len(sys.argv)>2) :
		do_api_tables =  do_api_tables_data = do_mapping_tables =  data_display =  do_campaign_mapping =  do_auth_table =  do_impression_log =  do_bid_log = do_cal_download_log = False
	
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
	elif o in ("-D"):
		debug = True
	elif o in ("-a"):
		do_api_tables = True
	elif o in ("-d"):
		do_api_tables_data = True
	elif o in ("-m"):
		do_mapping_tables = True
	elif o in ("-p"):
		data_display = True
	elif o in ("-c"):
		do_campaign_mapping = True
	elif o in ("-A"):
		do_auth_table = True
	elif o in ("-i"):
		do_impression_log = True
	elif o in ("-b"):
		do_bid_log = True
	elif o in ("-l"):
		do_cal_download_log = True
	else:
		if debug == True:
			display(debug=debug)
		assert False, "unhandled option"

def display(debug=False):
	if debug ==True:
		print("do_api_tables", do_api_tables)
		print("do_api_tables_data", do_api_tables_data)
		print("do_mapping_tables",do_mapping_tables)
		print("data_display", data_display)
		print("do_campaign_mapping ",do_campaign_mapping )
		print("do_auth_table", do_auth_table)
		print("do_impression_log",do_impression_log)
		print("do_bid_log",do_bid_log)
		print("do_cal_download_log",  do_cal_download_log) 
if debug == True:
	display(debug)
	
db_conn = get_mysql_connection()
if db_conn == None:
	print("Error cannot connect to MySQL database")

cursor = db_conn.cursor()

# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

if do_api_tables == True or do_api_tables_data == True or data_display == True:
	api_table = cal_api_to_db_table_mapping_table_name()
	if debug == True:
		print("api_table from cal_api_to_db_table_mapping_table_name() is",api_table)

if do_api_tables == True:
	api_sql = "create table "+api_table +" ( api varchar(60) NOT NULL, data_table varchar(60) NOT NULL, download_log_table varchar(60), PRIMARY KEY(api) ); "
	result = cursor.execute(api_sql)
	#db_conn.commit()
	if debug == True:
		print("result of SQL is",result)
	api_sql_grant = "grant select,update,insert on  prog_stats.prog_ix_api_to_db_table_mapping to iximport@localhost ;"
	result = cursor.execute(api_sql_grant)
	db_conn.commit()
	if debug == True:
		print("result of SQL for grant is",result)

if do_api_tables_data == True:
	# populate
	data = [ [ "api", "data_table", "download_log_table" ], ["impression_events", "prog_ix_impression_log", "prog_ix_impressions_event_fileid"],[ "bid_events","prog_ix_bid_log","prog_ix_bid_event_fileid"], [ "buyer_mapping","prog_ix_buyer_mapping","" ] , [ "campaign_mapping" , "campaign_mapping" , ""]  , [ "deal_mapping", "prog_ix_deal_mapping","" ] , [ "dsp_mapping","prog_ix_dsp_mapping",""],[ "site_mapping","prog_ix_site_mapping",""],[ "partner_mapping", "prog_ix_partner_mapping","" ] ]
	result = insert_csv_list_to_db(cursor,api_table,data)
	db_conn.commit()

if data_display == True:
	print(cal_api_to_db_table_mapping_table_name()+" table contents:")
	result = select_column_with_cursor(cursor,api_table,"*")
	for item in result:
		if debug == True:
			print("type: ",type(item)," len: ", len(item)," item: ",item)
		else:
			print(" item: ",item)

if do_auth_table == True:
	#auth_table_sql = "create table "+get_apikeys_table_name()+" ( publisher_id integer NOT NULL, api_key varchar(255) NOT NULL, PRIMARY KEY(publisher_id)); grant select,update,insert on  prog_stats.prog_ix_apikeys to iximport@localhost ; "
	auth_table_sql = "create table "+get_apikeys_table_name()+" ( publisher_id integer NOT NULL, api_key varchar(255) NOT NULL, PRIMARY KEY(publisher_id));"
	cursor.execute(auth_table_sql)
	auth_table_sql_grant = "grant select,update,insert on  prog_stats.prog_ix_apikeys to iximport@localhost ; "
	cursor.execute(auth_table_sql_grant)

if do_mapping_tables == True:
	#mapping_sql_dsp_mapping = "create table prog_ix_dsp_mapping ( dsp_id integer NOT NULL, dsp_name varchar(255), PRIMARY KEY(dsp_id)); commit; grant select,update,insert on prog_stats.prog_ix_dsp_mapping to iximport@localhost ; commit;"
	#mapping_sql_partner_mapping = "create table prog_ix_partner_mapping ( partner_id integer NOT NULL, partner_name varchar(255) NOT NULL, PRIMARY KEY(partner_id)); grant select,update,insert on  prog_stats.prog_ix_partner_mapping to iximport@localhost;"

	mapping_sql_buyer_mapping = "create table prog_ix_buyer_mapping ( dsp_id integer NOT NULL, trading_desk_id integer NOT NULL, buyer_name varchar(255) NOT NULL, PRIMARY KEY (dsp_id,trading_desk_id));"
	mapping_sql_buyer_mapping_grant = "grant select,update,insert on  prog_stats.prog_ix_buyer_mapping to iximport@localhost ;"
	mapping_sql_deal_mapping = "create table prog_ix_deal_mapping ( deal_id varchar(255) NOT NULL, internal_deal_id integer NOT NULL, deal_name varchar(255) NOT NULL, dsp_id integer NOT NULL, deal_type integer NOT NULL, auction_type varchar(255) NOT NULL, rate float NOT NULL, section_id varchar(255) NOT NULL, status char(1) NOT NULL, start_date date NOT NULL, end_date date NOT NULL, priority integer NOT NULL, publisher_id integer NOT NULL, PRIMARY KEY (internal_deal_id));"
	mapping_sql_deal_mapping_grant = "grant select,update,insert on prog_stats.prog_ix_deal_mapping to iximport@localhost ;"
	mapping_sql_dsp_mapping = "create table prog_ix_dsp_mapping ( dsp_id integer NOT NULL, dsp_name varchar(255), PRIMARY KEY(dsp_id));"
	mapping_sql_dsp_mapping_grant = "grant select,update,insert on prog_stats.prog_ix_dsp_mapping to iximport@localhost ;"
	mapping_sql_site_mapping = "create table prog_ix_site_mapping ( site_id integer NOT NULL, site_name varchar(255) NOT NULL, PRIMARY KEY(site_id));"
	mapping_sql_site_mapping_grant = "grant select,update,insert on  prog_stats.prog_ix_site_mapping to iximport@localhost ;"
	mapping_sql_partner_mapping = "create table prog_ix_partner_mapping ( partner_id integer NOT NULL, partner_name varchar(255) NOT NULL, PRIMARY KEY(partner_id));"
	mapping_sql_partner_mapping_grant = "grant select,update,insert on  prog_stats.prog_ix_partner_mapping to iximport@localhost;"

	for sql in (mapping_sql_buyer_mapping,mapping_sql_deal_mapping,mapping_sql_dsp_mapping,mapping_sql_site_mapping,mapping_sql_partner_mapping):
		if debug == True:
			print("implementing ",sql)
		result = cursor.execute(sql)
		#print(cursor.fetchall())
	db_conn.commit()
def do_grant():
	for sql in (mapping_sql_buyer_mapping_grant,mapping_sql_deal_mapping_grant,mapping_sql_dsp_mapping_grant,mapping_sql_site_mapping_grant,mapping_sql_partner_mapping_grant):
		if debug == True:
			print("implementing ",sql)
		cursor.execute(sql)
		print(cursor.fetchall())
	db_conn.commit()

if do_campaign_mapping == True:
	mapping_sql_creatives = "create table prog_ix_creatives ( creative_id integer NOT NULL, creative_name varchar(255) NOT NULL, PRIMARY KEY (creative_id));"
	mapping_sql_campaign_mapping = "create table prog_ix_campaign_mapping ( brand_id integer NOT NULL, brand_name varchar(255) NOT NULL, campaign_id integer NOT NULL, campaign_name varchar(255) NOT NULL, creative_id int NOT NULL, PRIMARY KEY (brand_id,campaign_id), FOREIGN KEY (creative_id) REFERENCES prog_ix_creatives(creative_id));"
	# grant select,update,insert on  prog_stats.prog_ix_campaign_mapping to iximport@localhost ;"
	mapping_sql_creatives_grant = "grant select,update,insert on prog_ix_creatives to iximport@localhost;"
	mapping_sql_campaign_mapping_grant = "grant select,update,insert on prog_ix_campaign_mapping to iximport@localhost;"

	#mapping_sql_creatives = "create table prog_ix_creatives ( creative_id integer NOT NULL, creative_name varchar(255) NOT NULL, PRIMARY KEY (creative_id));grant select,update,insert on prog_ix_creatives to iximport@localhost;"

	cursor.execute(mapping_sql_creatives)
	cursor.execute(mapping_sql_campaign_mapping)
	# db_conn.commit()
	cursor.execute(mapping_sql_creatives_grant)
	#db_conn.commit()
	cursor.execute(mapping_sql_campaign_mapping_grant)
	#db_conn.commit()

### log_sql_base = "CREATE TABLE prog_ix_impression_log ( auction_id varchar(36) NOT NULL default '', publisher_id int NOT NULL , timestamp timestamp NULL DEFAULT NULL, country varchar(2) DEFAULT '', state varchar(16) DEFAULT '', dma int NOT NULL, zip_postal varchar(32) DEFAULT '', device_type varchar(255) DEFAULT '', operating_system varchar(255) DEFAULT '', browser varchar(16) DEFAULT '', partner_id int NOT NULL, site_id int NOT NULL , creative_type varchar(16) DEFAULT '', domain varchar(255) DEFAULT '', app_bundle varchar(255) DEFAULT '', inventory_channel varchar(255) DEFAULT '', supply_source varchar(255) DEFAULT '', slot_id varchar(255) NOT NULL, size varchar(255) DEFAULT '', event_type varchar(255) DEFAULT '', event_opportunity varchar(255) DEFAULT '', gross_revenue decimal(10,5) NOT NULL DEFAULT '0.00000', net_revenue decimal(10,5) NOT NULL DEFAULT '0.00000', dsp_id int NOT NULL, trading_desk_id int NOT NULL, campaign_id int NOT NULL, campaign_name varchar(255) DEFAULT '', brand_id int NOT NULL, brand_name varchar(255) DEFAULT '', creative_id int NOT NULL, creative_name varchar(255) DEFAULT '', deal_id varchar(255) NOT NULL, internal_deal_id int NOT NULL, cookie_match_status varchar(255) DEFAULT '', a_domain varchar(255) DEFAULT '', pub_rev_share decimal(10,5) NOT NULL DEFAULT '0.00000', billing_term_id int NOT NULL, p_ids varchar(255) DEFAULT '', discount_amount decimal(10,5) NOT NULL DEFAULT '0.00000', video_placement_type varchar(255) DEFAULT '', other varchar(255) DEFAULT '' , PRIMARY KEY (auction_id) );"
log_sql_base = "( auction_id varchar(36) NOT NULL default '', publisher_id int NOT NULL , timestamp timestamp NULL DEFAULT NULL, country varchar(255) DEFAULT '', state varchar(255) DEFAULT '', dma int NOT NULL, zip_postal varchar(255) DEFAULT '', device_type varchar(255) DEFAULT '', operating_system varchar(255) DEFAULT '', browser varchar(255) DEFAULT '', partner_id int NOT NULL, site_id int NOT NULL , creative_type varchar(255) DEFAULT '', domain varchar(255) DEFAULT '', app_bundle varchar(255) DEFAULT '', inventory_channel varchar(255) DEFAULT '', supply_source varchar(255) DEFAULT '', slot_id int NOT NULL, size varchar(255) DEFAULT '', event_type varchar(255) DEFAULT '', event_opportunity varchar(255) DEFAULT '', gross_revenue decimal(10,5) NOT NULL DEFAULT '0.00000', net_revenue decimal(10,5) NOT NULL DEFAULT '0.00000', dsp_id int NOT NULL, trading_desk_id int NOT NULL, campaign_id int NOT NULL, campaign_name varchar(255) DEFAULT '', brand_id int NOT NULL, brand_name varchar(255) DEFAULT '', creative_id int NOT NULL, creative_name varchar(255) DEFAULT '', deal_id varchar(255) NOT NULL, internal_deal_id int NOT NULL, cookie_match_status varchar(255) DEFAULT '', a_domain varchar(255) DEFAULT '', pub_rev_share decimal(10,5) NOT NULL DEFAULT '0.00000', billing_term_id int DEFAULT '-1', p_ids varchar(255) DEFAULT '', discount_amount decimal(10,5) NOT NULL DEFAULT '0.00000', video_placement_type varchar(255) DEFAULT '', other varchar(255) DEFAULT '' , PRIMARY KEY (auction_id) );"
if do_impression_log == True:
	impression_log_sql = "CREATE TABLE prog_ix_impression_log "+log_sql_base
	impression_log_sql_grant = "grant select,update,insert on prog_stats.prog_ix_impression_log to iximport@localhost;"
	result = cursor.execute(impression_log_sql)
	if debug == True:
		print("impression_log_sql) result",result)

	db_conn.commit()
	result = cursor.execute(impression_log_sql_grant)
	if debug == True:
		print("impression_log_sql_grant) result",result)

if do_bid_log == True:
	bid_log_sql = "CREATE TABLE prog_ix_bid_log "+log_sql_base
	bid_log_sql_grant = "grant select,update,insert on prog_stats.prog_ix_bid_log to iximport@localhost;"
	result = cursor.execute(bid_log_sql)
	if debug == True:
		print("bid_log_sql) result",result)

	db_conn.commit()
	result = cursor.execute(bid_log_sql_grant)
	if debug == True:
		print("bid_log_sql_grant) result",result)

if do_cal_download_log == True:
	cal_download_log_sql = " create table prog_ix_cal_download_log ( fileid integer NOT NULL, hour datetime NOT NULL, downloadURL varchar(255) NOT NULL, publisher_id integer NOT NULL, origin varchar(255) NOT NULL, PRIMARY KEY(fileid, publisher_id));"
	cal_download_log_sql_grant = "grant select,update,insert on prog_stats.prog_ix_cal_download_log to iximport@localhost ;"
	result = cursor.execute(cal_download_log_sql)
	if debug == True:
		print("cal_download_log_sql) result",result)

	db_conn.commit()
	result = cursor.execute(cal_download_log_sql_grant)
	if debug == True:
		print("cal_download_log_sql_grant) result",result)

#Closing the connection(s)
cursor.close()
db_conn.close()
