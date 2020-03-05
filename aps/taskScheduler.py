from . import scheduler_helper
import datetime 
from rest_framework.response import Response
from rest_framework import status
import re
# DATEFORMAT - "2009-11-06 16:30:05"
# Scheduler -> 
#     Date Sched
#         -> Date job inputs
#               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int)
#     Interval Sched
#         -> Interval job inputs
#               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int), intv_seconds(int), intv_hours(int), intv_minutes(int), intv_weeks(int)
#     Cron Sched
#         -> Cron job inputs
#               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int), job_month(str), job_day(str), job_week(str), job_dow(str), job_seconds(str), job_minutes(str), job_hours(str) 

# sessionTimeout, API Versioning header based,

'''curl -d '{
     "correlationID":"1055",python
     "diagnosticsid":"1055",
     "starttime":"2020-03-02 19:40:10",
     "endtime" : "2020-10-02 20:18:10",
     "jobtype":"interval",
     "intv_time":"00:20:15"
 }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/'''

'''curl -d '{
      "diagnosticsid" : "1",
      "starttime" : "2020-02-24 13:20:10",
      "jobtype" : "date"
     }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/'''

# hostname,
# Retires, from UI
# No of instances, default value
#
# curl -d '{
#     "diagnosticsid":"4440",
#     "starttime":"2020-02-20 13:20:10",
#     "jobtype":"interval",
#     "intv_time":"00:00:5"
# }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/


# '{
#     "correlationID":"320",
#     "diagnosticsid":"320"
#     "startime":"09-02-2019 19:40:11",
#     "jobtype":"interval",
#     "interval": "{
#                 "seconds":"10",
#                 "hours":"22"
#                 }"
# }'
# curl -d '{"diagnosticsid":"1"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/remove
# curl -d '{"status":"state"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status
# curl -d '{"status":"start"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status
# curl  -H "Content-Type: application/json" -X GET localhost:8000/schedule/tasks
# curl -d '{"diagnosticsid":"1"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/fetch




 
#     currentDT = datetime.datetime.now()
#     print(diagID,"sendRequest()",currentDT.strftime("%Y-%m-%d %H:%M:%S") )


def dateformatter(cur_date):
    date_time = {
        "day": "",
        "date": "",
        "month": "",
        "year": "",
        "hour": "",
        "minutes": "",
        "seconds": ""
    }
    dt_obj = datetime.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
    date_time["date"] = dt_obj.strftime('%d')
    date_time["month"] = dt_obj.strftime('%m')
    date_time["year"] = dt_obj.strftime('%Y')
    date_time["hour"] = dt_obj.strftime('%H')
    date_time["minutes"] = dt_obj.strftime('%M')
    date_time["seconds"] = dt_obj.strftime('%S')

def timeformatter(cur_time):
    targetTime = str(cur_time)
    if re.match(r"\d\d:\d\d:\d\d",targetTime):
        hrs = targetTime[:2]
        min = targetTime[3:5]
        sec = targetTime[6:8]
        return (hrs,min,sec)
    else:
        return(None,None,None)

def scheduleJob(data):
    print("Processing request to scheduler ",data.data)
    r_data = data.data
    diagnosticsID = r_data['diagnosticsid'] if "diagnosticsid" in r_data else 0
    correlationID = r_data.get('correlationID')
    starttime = r_data['starttime'] if "starttime" in r_data else None
    endtime = r_data['endtime'] if "endtime" in r_data else None
    jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    
    ## INTERVAL JOB VARIABLES 
    intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0
    intv_time = r_data['intv_time'] if "intv_time" in r_data else None
    intv_hrs, intv_min, intv_sec = timeformatter(intv_time) 

    ## Add format check for intv_time 

    # intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
    # intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
    # intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
    
    
    ## CRONJOB VARIABLES
    # job_month, job_day, job_week, job_dow, job_seconds, job_minutes, job_hours
    job_month = r_data['job_month'] if "job_month" in r_data else None
    job_day = r_data['job_day'] if "job_day" in r_data else None
    job_week = r_data['job_week'] if "job_week" in r_data else None
    job_year = r_data['job_year'] if "job_year" in r_data else None
    job_dow = r_data['job_dow'] if "job_dow" in r_data else None
    job_sec = r_data['job_seconds'] if "job_seconds" in r_data else None
    job_min = r_data['job_minutes'] if "job_minutes" in r_data else None
    job_hrs = r_data['job_hours'] if "job_hours" in r_data else None
    enddate = r_data['enddate'] if "enddate" in r_data else None


    # start date
    if diagnosticsID == 0 :
        return ("Diagnostic ID is required", status.HTTP_400_BAD_REQUEST)
    else:
        if jobtype == 'date':
            if starttime != None:
                if scheduler_helper.get_job(str(diagnosticsID)) == None:
                    job = scheduler_helper.add_DateJob(starttime,diagnosticsID,correlationID)
                    return (True,"Date job scheduled!", status.HTTP_201_CREATED)
                elif scheduler_helper.get_job(str(diagnosticsID)) != None:
                    return (False,"Job with Diagnostic ID already exists", status.HTTP_400_BAD_REQUEST )
            elif starttime == None:
                return (False,"Date field can't be empty for date jobs", status.HTTP_400_BAD_REQUEST)

        elif jobtype == 'interval':
            # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
            print(starttime, intv_hrs, intv_min)
            if starttime != None and intv_sec != None and intv_hrs != None and intv_min != None :
                if scheduler_helper.get_job(str(diagnosticsID)) == None:
                    job = scheduler_helper.add_IntervalJob(
                                            intv_sec,
                                            intv_min,
                                            intv_hrs,
                                            intv_weeks,
                                            starttime,
                                            diagnosticsID,correlationID)
                    
                    return (True, "Interval job scheduled!", status.HTTP_201_CREATED)
                elif scheduler_helper.get_job(str(diagnosticsID)) != None:
                    return (False, "Job with diagnostic ID already exists", status.HTTP_400_BAD_REQUEST)
            elif starttime == None:
                return (False,"Startdate is required for scheduling!", status.HTTP_400_BAD_REQUEST)
            else:
                return (False,"Error in scheduling job", status.HTTP_400_BAD_REQUEST)

            # return "job details: %s" % job

        elif jobtype == 'cron':
            # hour,min,sec -> int // year,month,day,week,dayofweek
            if starttime != None:
                if scheduler_helper.get_job(str(diagnosticsID)) == None:
                    job = scheduler_helper.add_CronJob(
                                        job_year,
                                        job_month, 
                                        job_day, 
                                        job_week,
                                        job_dow,
                                        job_hrs,
                                        job_min,
                                        job_sec,
                                        starttime,
                                        enddate,
                                        diagnosticsID,
                                        correlationID)
                    return (True,"Cron job scheduled!", status.HTTP_201_CREATED)
                elif scheduler_helper.get_job(str(diagnosticsID)) != None:
                    return (False,"Job with diagnostic ID already exists", status.HTTP_400_BAD_REQUEST)
            elif starttime == None:
                return (False,"Specify a startdate", status.HTTP_400_BAD_REQUEST)


def updateJob(data):
    print("Processing request to scheduler ",data.data)
    r_data = data.data
    diagnosticsID = r_data['diagnosticsid'] if "diagnosticsid" in r_data else 0
    correlationID = r_data.get('correlationID')
    starttime = r_data['starttime'] if "starttime" in r_data else None
    endtime = r_data['endtime'] if "endtime" in r_data else None
    jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    
    ## INTERVAL JOB VARIABLES 
    intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0
    intv_time = r_data['intv_time'] if "intv_time" in r_data else None
    intv_hrs, intv_min, intv_sec = timeformatter(intv_time) 

    ## Add format check for intv_time 

    # intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
    # intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
    # intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
    
    
    ## CRONJOB VARIABLES
    # job_month, job_day, job_week, job_dow, job_seconds, job_minutes, job_hours
    job_month = r_data['job_month'] if "job_month" in r_data else None
    job_day = r_data['job_day'] if "job_day" in r_data else None
    job_week = r_data['job_week'] if "job_week" in r_data else None
    job_year = r_data['job_year'] if "job_year" in r_data else None
    job_dow = r_data['job_dow'] if "job_dow" in r_data else None
    job_sec = r_data['job_seconds'] if "job_seconds" in r_data else None
    job_min = r_data['job_minutes'] if "job_minutes" in r_data else None
    job_hrs = r_data['job_hours'] if "job_hours" in r_data else None
    enddate = r_data['enddate'] if "enddate" in r_data else None


    # start date
    if diagnosticsID == 0 :
        return ("Diagnostic ID is required", status.HTTP_400_BAD_REQUEST)
    else:
        if jobtype == 'date':
            if starttime != None:
                if scheduler_helper.get_job(str(diagnosticsID)) != None:
                    job = scheduler_helper.update_DateJob(starttime,diagnosticsID,correlationID)
                    return (True,"Date job rescheduled!", status.HTTP_201_CREATED)
                elif scheduler_helper.get_job(str(diagnosticsID)) == None:
                    return (False,"Job with Diagnostic ID does not exist", status.HTTP_400_BAD_REQUEST )
            elif starttime == None:
                return (False,"Date field can't be empty for date jobs", status.HTTP_400_BAD_REQUEST)

        elif jobtype == 'interval':
            # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
            
            if starttime != None and intv_sec != None and intv_hrs != None and intv_min != None :
                if scheduler_helper.get_job(str(diagnosticsID)) != None:
                    job = scheduler_helper.update_IntervalJob(
                                            intv_sec,
                                            intv_min,
                                            intv_hrs,
                                            intv_weeks,
                                            starttime,
                                            diagnosticsID)
                    
                    return (True, "Interval job rescheduled!", status.HTTP_201_CREATED)
                elif scheduler_helper.get_job(str(diagnosticsID)) == None:
                    return (False, "Job with diagnostic ID does not exist", status.HTTP_400_BAD_REQUEST)
            elif starttime == None:
                return (False,"Startdate is required for rescheduling!", status.HTTP_400_BAD_REQUEST)
            else:
                return (False,"Error in rescheduling job", status.HTTP_400_BAD_REQUEST)

            # return "job details: %s" % job

        elif jobtype == 'cron':
            # hour,min,sec -> int // year,month,day,week,dayofweek
            if starttime != None:
                if scheduler_helper.get_job(str(diagnosticsID)) != None:
                    job = scheduler_helper.update_CronJob(
                                        job_year,
                                        job_month, 
                                        job_day, 
                                        job_week,
                                        job_dow,
                                        job_hrs,
                                        job_min,
                                        job_sec,
                                        starttime,
                                        enddate,
                                        diagnosticsID)
                    return (True,"Cron job rescheduled!", status.HTTP_201_CREATED)
                elif scheduler_helper.get_job(str(diagnosticsID)) == None:
                    return (False,"Job with diagnostic ID does not exist", status.HTTP_400_BAD_REQUEST)
            elif starttime == None:
                return (False,"Specify a startdate", status.HTTP_400_BAD_REQUEST)


 