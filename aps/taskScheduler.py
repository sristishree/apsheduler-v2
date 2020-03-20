from . import scheduler_helper
import datetime 
from rest_framework.response import Response
from rest_framework import status
import re
from .schedulerPack import schedPack
import ruamel.yaml

'''curl -d '{
     "correlationID":"",
     "diagnosticsid":"132",
     "starttime":"2020-03-05 19:40:10",
     "endtime" : "2020-10-02 20:18:10",
     "jobtype":"interval",
     "intv_weeks":"2",
     "intv_days":"4",
     "target":{target_env:"windows", host:"testzbxsvr"},
     "intv_time":"00:01:30"
 }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/'''

 
'''curl -d '{
     "correlationID":"",
     "diagnosticsid":"12",
     "starttime":"2020-03-05 19:40:10",
     "endtime" : "2020-10-02 20:18:10",
     "jobtype":"cron",
     "job_hours":"20",
     "job_minutes":"30"
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
#     "intv_time":"00:00:10"
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


### ====================== ###
### BEGIN HELPER FUNCTIONS ###
### ====================== ###

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

def gen_schedulerID():
    schedID = 'sched_'+uuid.uuid4().hex[:10]
    return(schedID)

def timeformatter(cur_time):
    targetTime = str(cur_time)
    if re.match(r"\d\d:\d\d:\d\d",targetTime):
        hrs = targetTime[:2]
        mins = targetTime[3:5]
        sec = targetTime[6:8]
        return (hrs,mins,sec)
    elif re.match(r"\d\d:\d\d",targetTime):
        hrs = targetTime[:2]
        mins = targetTime[3:5]
        sec = 00
        return (hrs,mins,sec)
    else:
        return(None,None,None)

def cronDateFormatter(cur_date):
    targetDate = str(cur_date)
    if re.match(r"^(\*{1}|\d{4})\-(\*|\d{2})\-(\*|\d{2})$",targetDate):
        year,month,date= targetDate.split("-")
        return (year,month,date)
    else:
        return(None,None,None)

def cronTimeFormatter(cur_time):
    targetTime = str(cur_time)
    if re.match(r"^(\*{1}|\d{2})\-(\*|\d{2})\-(\*|\d{2})$",targetTime):
        hour,minutes,seconds= targetTime.split("-")
        return (hour,minutes,seconds)
    else:
        return(None,None,None)

def initializationTimeFormatter(ui_time):
    ct = str(ui_time)
    time_format = ct.replace("T"," ")
    if re.match(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d",time_format):
        return (time_format)
    elif re.match(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d",time_format):
        sec = ':00'
        time_format = time_format + sec
        return (time_format)


### ======================= ###
### END OF HELPER FUNCTIONS ###
### ======================= ###    

def scheduleJob(data):
    print("Processing request to scheduler ",data.data)
    r_data = data.data
    diagnosticsID = r_data['diagnosticsid'] if "diagnosticsid" in r_data else 0
    correlationID = r_data.get('correlationID')

    target = r_data['target'] if "target" in r_data else None
    #yaml = ruamel.yaml.YAML(typ='safe')
    #target = yaml.load(target)
    print(target)
    target_env = target['target_env'] if "target_env" in target else None
    ip = target['host'] if "host" in target else None


    starttime_ui = r_data['starttime'] if "starttime" in r_data else None
    endtime_ui = r_data['endtime'] if "endtime" in r_data else None
    jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    schedID  = r_data['schedulerID'] 
    schedName = r_data['schedulerName'] if "schedulerName" in r_data else target_env+'_'+jobtype+'_'+schedID


    starttime = initializationTimeFormatter(starttime_ui)
    endtime = initializationTimeFormatter(endtime_ui)

    '''
    Creating Dict for UI Scheduling Data
    '''

    uiData = r_data
    print(uiData)
    del uiData['correlationID'] 

    if diagnosticsID == 0 :
        return (False, "Diagnostic ID is required", 400)
    else:
        if jobtype == 'date':
            
            '''
            Initialize variables for Date Job
            '''

            if starttime != None:
                job = scheduler_helper.add_DateJob(starttime,diagnosticsID,correlationID,schedName,schedID,target_env,ip)
                
                '''
                Create data for scheduler pack
                '''

                pobj = schedPack()
                pobj.create_schedPack(jobtype,
                        diagID=diagnosticsID,
                        starttime=starttime,
                        request=uiData,
                        schedID=schedID,
                        schedName=schedName
                        )
                return (True,"Date job scheduled!",201)
            
            elif starttime == None:
                return (False,"Date field can't be empty for date jobs", 400)

        elif jobtype == 'interval':

            
            '''
            Initialize variables for Interval Job
            '''

            intv_time = r_data['intv_time']
            intv_hrs, intv_min, intv_sec = timeformatter(intv_time) 
            intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data and r_data['intv_weeks'] != "" else 0
            intv_days = int(r_data['intv_days']) if "intv_days" in r_data and r_data['intv_days'] != "" else 0

            if starttime != None and intv_sec != None and intv_hrs != None and intv_min != None :
                job = scheduler_helper.add_IntervalJob(
                                        intv_sec,
                                        intv_min,
                                        intv_hrs,
                                        intv_weeks,
                                        intv_days,
                                        starttime,
                                        endtime,
                                        diagnosticsID,correlationID,
                                        schedName,
                                        schedID,
                                        target_env,ip
                                        )

                '''
                Create data for scheduler pack
                '''

                pobj = schedPack()
                pobj.create_schedPack(jobtype,
                        diagID=diagnosticsID,
                        starttime=starttime,
                        hours=intv_hrs,
                        minutes=intv_min,
                        seconds=intv_sec,
                        weeks=intv_weeks,
                        day=intv_days,
                        request=uiData,
                        schedID=schedID,
                        schedName=schedName
                        )

                return (True, "Interval job scheduled!", 201)
            elif starttime == None:
                return (False,"Startdate is required for scheduling!", 400)
            else:
                return (False,"Error in scheduling job",400)


        elif jobtype == 'cron':
            
            '''
            Initialize variables for Cron Job
            '''

            cron_date = r_data['date'] if 'date' in r_data else None 
            cron_time = r_data['time'] if 'time' in r_data else None
            job_year,job_month,job_day = cronDateFormatter(cron_date)
            
            job_hrs,job_min,job_sec = cronTimeFormatter(cron_time)
            
            job_week = r_data['job_week'] if "job_week" in r_data else None
            
            job_dow = r_data['dow'] if "dow" in r_data and r_data['dow'] !='' else None

            if job_dow != None:
                job_dow = job_dow.lower()[:3]

            if starttime != None:
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
                                    endtime,
                                    diagnosticsID,correlationID,
                                    schedName,
                                    schedID,
                                    target_env,ip
                                    )

                '''
                Create data for scheduler pack
                '''

                pobj = schedPack()
                pobj.create_schedPack(jobtype,
                        diagID=diagnosticsID,
                        starttime=starttime,
                        hours=job_hrs,
                        minutes=job_min,
                        seconds=job_sec,
                        year=job_year,
                        month=job_month,
                        day=job_day,
                        week=job_week,
                        day_of_week=job_dow,
                        endtime=endtime,
                        request=uiData,
                        schedID=schedID,
                        schedName=schedName
                        )

                return (True,"Cron job scheduled!", 201)
                
            elif starttime == None:
                return (False,"Specify a startdate", 400)




 