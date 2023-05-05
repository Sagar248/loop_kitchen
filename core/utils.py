import csv
import pytz
import datetime
from datetime import datetime as dt, timedelta

from . models import OpenHours, OpenHoursUTC, StoreStatus

def process_open_hours():
    with open("./open_hours.csv", 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            store_id = row[0]
            day = row[1]
            local_open_time = row[2]
            local_close_time = row[3]
            store = OpenHours.objects.create(store_id=store_id, day = day, 
                                             local_open_time=local_open_time, local_close_time=local_close_time)
            
    
def process_open_hours_utc():
    with open("./store_timezone.csv", 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)
        for row in csvreader:
            store_id = row[0]
            timezone_str = row[1]    
            stores = OpenHours.objects.filter(store_id=store_id)
            for s in stores:
                local_day = s.day
                local_open_time = s.local_open_time
                local_close_time = s.local_close_time
                utc_open_time = get_utc_time(timezone_str, local_day, local_open_time.hour, local_open_time.minute)
                utc_close_time = get_utc_time(timezone_str, local_day, local_open_time.hour, local_open_time.minute)
                open_time_day = utc_open_time.day if utc_open_time.day!=7 else 0
                close_time_day = utc_close_time.day if utc_close_time.day!=7 else 0
                if(utc_open_time.day!=utc_close_time.day):
                    store = OpenHoursUTC.objects.create(store_id=store_id, day = open_time_day, 
                                                        utc_open_time=datetime.time(utc_open_time.hour, utc_open_time.minute),
                                                        utc_close_time=datetime.time(23, 59))
                    store = OpenHoursUTC.objects.create(store_id=store_id, day = close_time_day, 
                                                        utc_open_time=datetime.time(00, 00),
                                                        utc_close_time=datetime.time(utc_close_time.hour, utc_close_time.minute))
                else:
                    store = OpenHoursUTC.objects.create(store_id=store_id, day = utc_open_time.day, 
                                                        utc_open_time=datetime.time(utc_open_time.hour, utc_open_time.minute),
                                                        utc_close_time=datetime.time(utc_close_time.hour, utc_close_time.minute))

def get_utc_time(timezone_str, day, hour, minute):
    tz = pytz.timezone(timezone_str)
    local_time = dt.now(tz)  # Get current local time in the given timezone
    if(day==0):
        day=day+7
    local_time = local_time.replace(day=day, hour=hour, minute=minute, second=0, microsecond=0) # Set the given hour and minute
    utc_time = local_time.astimezone(pytz.utc)  # Convert local time to UTC time
    return utc_time

def process_store_status():
        with open("./store_status.csv", 'r') as file:
            csvreader = csv.reader(file)
            next(csvreader)
            for row in csvreader:
                store_id = row[0]
                status = row[1]
                timestamp_utc = row[2]
                datetime_obj = datetime.datetime.strptime(timestamp_utc, '%Y-%m-%d %H:%M:%S.%f %Z')
                store = StoreStatus.objects.create(store_id=store_id, status = status, 
                                                   timestamp_utc=datetime_obj)
        
    

