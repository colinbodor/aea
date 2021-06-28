#!/usr/bin/python3
# MySQL:
# create database aprs;
# CREATE USER 'aprs'@'localhost' IDENTIFIED BY 'mypass';
# CREATE USER 'aprs'@'%' IDENTIFIED BY 'mypass';
# GRANT ALL ON *.* TO 'myuser'@'localhost';
# GRANT ALL ON *.* TO 'myuser'@'%';
# flush privileges;

# CREATE TABLE `abroads` (
#   `id` int NOT NULL,
#   `abid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
#   `organization` varchar(255) NOT NULL,
#   `roadwayname` varchar(255) NOT NULL,
#   `directionoftravel` varchar(255) NOT NULL,
#   `description` text NOT NULL,
#   `reported` varchar(255) NOT NULL,
#   `lastupdated` varchar(255) NOT NULL,
#   `startdate` varchar(255) NOT NULL,
#   `plannedenddate` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
#   `lanesaffected` varchar(255) NOT NULL,
#   `latitude` varchar(255) NOT NULL,
#   `longitude` varchar(255) NOT NULL,
#   `latitudesecondary` varchar(255) NOT NULL,
#   `longitudesecondary` varchar(255) NOT NULL,
#   `eventtype` varchar(255) NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

# CREATE TABLE `log` (
#   `id` int NOT NULL,
#   `process` varchar(255) NOT NULL,
#   `events` int NOT NULL,
#   `rundate` datetime NOT NULL
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



import pymysql, os, json, urllib.request, csv, io
from datetime import datetime

with urllib.request.urlopen("https://511.alberta.ca/api/v2/get/event") as abroad_url:
  abroad_data = json.loads(abroad_url.read().decode())

url = "https://wildfire.alberta.ca/reports/activedd.csv"
webpage = urllib.request.urlopen(url)
abfire_data = csv.reader(webpage.read().decode('utf-8').splitlines())

dbname = "aprs"
dbuser = "aprs"
dbpass = "Ax93=D#b"



# do validation and checks before insert
def validate_string(val):
   if val != None:
        if type(val) is int:
            #for x in val:
            #   print(x)
            return str(val).encode('utf-8')
        else:
            return val


# connect to MySQL
con = pymysql.connect(host = 'localhost',user = dbuser,passwd = dbpass,db = dbname)
cursor = con.cursor()

# define some things
now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

# parse the AB road json data and insert
count=0
cursor.execute("TRUNCATE abroads")
for i, item in enumerate(abroad_data):
    abid = validate_string(item.get("ID", None))
    organization = validate_string(item.get("Organization", None))
    roadwayname = validate_string(item.get("RoadwayName", None))
    directionoftravel = validate_string(item.get("DirectionOfTravel", None))
    description = validate_string(item.get("Description", None))
    reported = validate_string(item.get("Reported", None))
    lastupdated = validate_string(item.get("LastUpdated", None))
    startdate = validate_string(item.get("StartDate", None))
    plannedenddate = validate_string(item.get("PlannedEndDate", None))
    lanesaffected = validate_string(item.get("LanesAffected", None))
    latitude = validate_string(item.get("Latitude", None))
    longitude = validate_string(item.get("Longitude", None))
    latitudesecondary = validate_string(item.get("LatitudeSecondary", None))
    longitudesecondary = validate_string(item.get("LongitudeSecondary", None))
    eventtype = validate_string(item.get("EventType", None))
    cursor.execute("INSERT INTO abroads (abid, organization, roadwayname, directionoftravel, description, reported, lastupdated, startdate, plannedenddate, lanesaffected, latitude, longitude, latitudesecondary, longitudesecondary, eventtype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (abid, organization, roadwayname, directionoftravel, description, reported, lastupdated, startdate, plannedenddate, lanesaffected, latitude, longitude, latitudesecondary, longitudesecondary, eventtype))
    count +=1

# write out the log so we know what happened
cursor.execute("INSERT INTO log (process, events, rundate) VALUES ('abroads', %s, %s)", (count, formatted_date))


# parse the AB wildfire CSV data and insert
count=0
cursor.execute("TRUNCATE abfire")
next(abfire_data)
for row in abfire_data:
    name = (row[0])
    yesterday_datetime = (row[1])
    location = (row[2])
    description = (row[3])
    fire_number = (row[4])
    year = (row[5])
    fire_num_yr = (row[6])
    assessment_datetime = (row[7])
    fire_location_latitude = (row[8])
    fire_location_longitude = (row[9])
    general_cause = (row[10])
    cr_id = (row[11])
    id1 = (row[12])
    id2 = (row[13])
    percent_contained = (row[14])
    fire_status = (row[15])
    area_burned = (row[16])
    no_of_wfu = (row[17])
    no_of_manpower = (row[18])
    no_of_ag = (row[19])
    no_of_aircraft = (row[20])
    no_of_equipment = (row[21])
    no_of_ac_rw_light = (row[22])
    no_of_ac_rw_medium = (row[23])
    no_of_ac_rw_inter = (row[24])
    no_of_veq_truck = (row[25])
    no_of_veq_truck_wt = (row[26])
    no_of_veq_skidder = (row[27])
    no_of_veq_bus = (row[28])
    no_of_veq_dozer = (row[29])
    no_of_fl_eq_pump = (row[30])
    cr_group_name = (row[31])
    report_creation_date = (row[32])
    eco_zone_flag = (row[33])
    modified_action_flag = (row[34])
    web_general_cause = (row[35])
    fire_type = (row[36])
    group_type = (row[37])
    group_sort_1 = (row[38])
    fire_complex_number = (row[39])
    fire_complex_name = (row[40])
    fire_complex_year = (row[41])

    cursor.execute("INSERT INTO abfire (name, yesterday_datetime, location, description, fire_number, year, fire_num_yr, assessment_datetime, fire_location_latitude, fire_location_longitude, general_cause, cr_id, id1, id2, percent_contained, fire_status, area_burned, no_of_wfu, no_of_manpower, no_of_ag, no_of_aircraft, no_of_equipment, no_of_ac_rw_light, no_of_ac_rw_medium, no_of_ac_rw_inter, no_of_veq_truck, no_of_veq_truck_wt, no_of_veq_skidder, no_of_veq_bus, no_of_veq_dozer, no_of_fl_eq_pump, cr_group_name, report_creation_date, eco_zone_flag, modified_action_flag, web_general_cause, fire_type, group_type, group_sort_1, fire_complex_number, fire_complex_name, fire_complex_year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, yesterday_datetime, location, description, fire_number, year, fire_num_yr, assessment_datetime, fire_location_latitude, fire_location_longitude, general_cause, cr_id, id1, id2, percent_contained, fire_status, area_burned, no_of_wfu, no_of_manpower, no_of_ag, no_of_aircraft, no_of_equipment, no_of_ac_rw_light, no_of_ac_rw_medium, no_of_ac_rw_inter, no_of_veq_truck, no_of_veq_truck_wt, no_of_veq_skidder, no_of_veq_bus, no_of_veq_dozer, no_of_fl_eq_pump, cr_group_name, report_creation_date, eco_zone_flag, modified_action_flag, web_general_cause, fire_type, group_type, group_sort_1, fire_complex_number, fire_complex_name, fire_complex_year))
    count +=1

# write out the log so we know what happened
cursor.execute("INSERT INTO log (process, events, rundate) VALUES ('abfire', %s, %s)", (count, formatted_date))


con.commit()
con.close()

