# from .scheduler import scheduler
# import datetime 
# from rest_framework.response import Response
# from rest_framework import status
# import re
# # DATEFORMAT - "2009-11-06 16:30:05"
# # Scheduler -> 
# #     Date Sched
# #         -> Date job inputs
# #               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int)
# #     Interval Sched
# #         -> Interval job inputs
# #               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int), intv_seconds(int), intv_hours(int), intv_minutes(int), intv_weeks(int)
# #     Cron Sched
# #         -> Cron job inputs
# #               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int), job_month(str), job_day(str), job_week(str), job_dow(str), job_seconds(str), job_minutes(str), job_hours(str) 

# # sessionTimeout, API Versioning header based,

# # curl -d '{
# #     "correlationID":"051",
# #     "starttime":"2019-10-02 19:40:10",
# #     "endtime" : "2020-10-02 20:18:10"
# #     "command":"get-ip",
# #     "jobtype":"interval",
# #     "intv_seconds":"15"
# # }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/

# # curl -d '{
# #      "coid" : "469",
# #      "starttime" : "2020-02-24 13:20:10",
# #      "command" : "commandID",
# #      "jobtype" :
# #     }'

# # curl -d '{
# #     "coid":"140",
# #     "starttime":"2020-02-20 13:20:10",
# #     "command":"get-ip",
# #     "jobtype":"interval",
# #     "intv_time":"00:00:20"
# # }' -H "Content-Type: application/json" -X POST http://localhost:8001/schedule/


# # '{
# #     "correlationID":"320",
# #     "startime":"09-02-2019 19:40:11",
# #     "commandID":"get-ip",
# #     "jobtype":"interval",
# #     "interval": "{
# #                 "seconds":"10",
# #                 "hours":"22"
# #                 }"
# # }'
# # curl -d '{"job_id":"210"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/remove/
# # curl -d '{"status":"state"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status/
# # curl -d '{"status":"start"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status/
# # curl  -H "Content-Type: application/json" -X GET localhost:8000/schedule/tasks/





# def sendRequest(diagID):
#     # headers = {'Content-Type': 'application/json'}
#     # data = { 
#     #     "diagID" : diagID,
#     # }
#     # url = 'localhost:8000/' 
#     currentDT = datetime.datetime.now()
#     print(diagID,"sendRequest()",currentDT.strftime("%Y-%m-%d %H:%M:%S") )


# def dateformatter(cur_date):
#     date_time = {
#         "day": "",
#         "date": "",
#         "month": "",
#         "year": "",
#         "hour": "",
#         "minutes": "",
#         "seconds": ""
#     }
#     dt_obj = datetime.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
#     date_time["date"] = dt_obj.strftime('%d')
#     date_time["month"] = dt_obj.strftime('%m')
#     date_time["year"] = dt_obj.strftime('%Y')
#     date_time["hour"] = dt_obj.strftime('%H')
#     date_time["minutes"] = dt_obj.strftime('%M')
#     date_time["seconds"] = dt_obj.strftime('%S')

# def timeformatter(cur_time):
#     targetTime = str(cur_time)
#     if re.match(r"\d\d:\d\d:\d\d",targetTime):
#         hrs = targetTime[:2]
#         min = targetTime[3:5]
#         sec = targetTime[6:8]
#         return (hrs,min,sec)
#     else:
#         return(None,None,None)

# def scheduleJob(data):
#     print("Added request to scheduler ",data.data)
#     r_data = data.data
#     diagID = r_data['diagID'] if "diagID" in r_data else 0
#     starttime = r_data['starttime'] if "starttime" in r_data else None
#     endtime = r_data['endtime'] if "endtime" in r_data else None
#     cmd = r_data['command'] if "command" in r_data else None
#     jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    
#     ## INTERVAL JOB VARIABLES 
#     intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0
#     intv_time = r_data['intv_time'] if "intv_time" in r_data else None
#     intv_hrs, intv_min, intv_sec = timeformatter(intv_time) 

#     ## Add format check for intv_time 

#     # intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
#     # intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
#     # intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
    
    
#     ## CRONJOB VARIABLES
#     # job_month, job_day, job_week, job_dow, job_seconds, job_minutes, job_hours
#     job_month = r_data['job_month'] if "job_month" in r_data else None
#     job_day = r_data['job_day'] if "job_day" in r_data else None
#     job_week = r_data['job_week'] if "job_week" in r_data else None
#     job_year = r_data['job_year'] if "job_year" in r_data else None
#     job_dow = r_data['job_dow'] if "job_dow" in r_data else None
#     job_sec = r_data['job_seconds'] if "job_seconds" in r_data else None
#     job_min = r_data['job_minutes'] if "job_minutes" in r_data else None
#     job_hrs = r_data['job_hours'] if "job_hours" in r_data else None
#     enddate = r_data['enddate'] if "enddate" in r_data else None


#     # start date
#     if diagID == 0 :
#         return Response("Diagnostic ID is required", status=status.HTTP_400_BAD_REQUEST)
#     else:
#         if jobtype == 'date':
#             if starttime != 'None':
#                 job = scheduler.add_job(sendRequest, trigger='date', run_date=starttime,args=[diagID], id=str(diagID))
#                 return Response("Date job scheduled!", status=status.HTTP_201_CREATED)
#             elif starttime == 'None':
#                 return Response("Date field can't be empty for date jobs", status=status.HTTP_400_BAD_REQUEST)

#         elif jobtype == 'interval':
#             # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
            
#             if starttime != None and intv_sec != None and intv_hrs != None and intv_min != None :
#                 job = scheduler.add_job(sendRequest, trigger='interval',
#                                     seconds=int(intv_sec),
#                                     minutes=int(intv_min),
#                                     hours = int(intv_hrs),
#                                     weeks = intv_weeks,
#                                     start_date=starttime,
#                                     id=str(diagID), args=[diagID],
#                                     replace_existing=True)
                
#                 return Response("Interval job scheduled!", status=status.HTTP_201_CREATED)
#             elif starttime == None:
#                 return Response("Startdate is required for scheduling!", status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response("Error in scheduling job", status=status.HTTP_400_BAD_REQUEST)

#             # return "job details: %s" % job

#         elif jobtype == 'cron':
#             # hour,min,sec -> int // year,month,day,week,dayofweek
#             if starttime != None:
#                 job = scheduler.add_job(sendRequest, trigger='cron',
#                                     year=job_year,
#                                     month=job_month, 
#                                     day=job_day, 
#                                     week=job_week,
#                                     day_of_week=job_dow,
#                                     hour=job_hrs,
#                                     minute=job_min,
#                                     second=job_sec,
#                                     start_date=starttime,
#                                     end_date=enddate,
#                                     id=str(diagID), args=[diagID],
#                                     replace_existing=True)
#                 return Response("Cron job scheduled!", status=status.HTTP_201_CREATED)

#             elif starttime == None:
#                 return Response("Specify a startdate", status=status.HTTP_400_BAD_REQUEST)



# ================================================================================================
# ================================================================================================


# from .scheduler import scheduler
# import datetime 
# from rest_framework.response import Response
# from rest_framework import status
# import re
# # DATEFORMAT - "2009-11-06 16:30:05"
# # Scheduler -> 
# #     Date Sched
# #         -> Date job inputs
# #               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int)
# #     Interval Sched
# #         -> Interval job inputs
# #               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int), intv_seconds(int), intv_hours(int), intv_minutes(int), intv_weeks(int)
# #     Cron Sched
# #         -> Cron job inputs
# #               -> starttime*(str/datetime str), endtime(str/datetime str), id*(int), job_month(str), job_day(str), job_week(str), job_dow(str), job_seconds(str), job_minutes(str), job_hours(str) 

# # sessionTimeout, API Versioning header based,

# # curl -d '{
# #     "correlationID":"051",
# #     "starttime":"2019-10-02 19:40:10",
# #     "endtime" : "2020-10-02 20:18:10"
# #     "command":"get-ip",
# #     "jobtype":"interval",
# #     "intv_seconds":"15"
# # }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/

# # curl -d '{
# #      "coid" : "469",
# #      "starttime" : "2020-02-24 13:20:10",
# #      "command" : "commandID",
# #      "jobtype" :
# #     }'
# #
# # hostname,
# # Retires, from UI
# # No of instances, default value
# #
# # curl -d '{
# #     "coid":"4440",
# #     "starttime":"2020-02-20 13:20:10",
# #     "command":"get-ip",
# #     "jobtype":"interval",
# #     "intv_time":"00:00:20"
# # }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule/


# # '{
# #     "correlationID":"320",
# #     "startime":"09-02-2019 19:40:11",
# #     "commandID":"get-ip",
# #     "jobtype":"interval",
# #     "interval": "{
# #                 "seconds":"10",
# #                 "hours":"22"
# #                 }"
# # }'
# # curl -d '{"job_id":"210"}' -H "Content-Type: application/json" -X POST localhost:8001/schedule/remove/
# # curl -d '{"status":"state"}' -H "Content-Type: application/json" -X POST localhost:8000/schedule/status/
# # curl -d '{"status":"start"}' -H "Content-Type: application/json" -X POST localhost:8001/schedule/status/
# # curl  -H "Content-Type: application/json" -X GET localhost:8001/schedule/tasks/





# def sendRequest(diagID):
    
#     # headers = {'Content-Type': 'application/json'}
#     # params = { 
#     #     "diagID" : diagID,
#     #     "diagnostic_flag" : "True/False"(str),
#     #     "state_id": "int"<Unique ID> Lookup
#     #     "counter_": "int" Incremental
#     # }
#     # url = 'localhost:8000/' 
#     # res = requests.get(url,  headers=headers, params=params)
#     # scheduler_event(callback, arguments=[], MASK= EVENTS_ALL)
#     currentDT = datetime.datetime.now()
#     print(diagID,"sendRequest()",currentDT.strftime("%Y-%m-%d %H:%M:%S") )


# def dateformatter(cur_date):
#     date_time = {
#         "day": "",
#         "date": "",
#         "month": "",
#         "year": "",
#         "hour": "",
#         "minutes": "",
#         "seconds": ""
#     }
#     dt_obj = datetime.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
#     date_time["date"] = dt_obj.strftime('%d')
#     date_time["month"] = dt_obj.strftime('%m')
#     date_time["year"] = dt_obj.strftime('%Y')
#     date_time["hour"] = dt_obj.strftime('%H')
#     date_time["minutes"] = dt_obj.strftime('%M')
#     date_time["seconds"] = dt_obj.strftime('%S')

# def timeformatter(cur_time):
#     targetTime = str(cur_time)
#     if re.match(r"\d\d:\d\d:\d\d",targetTime):
#         hrs = targetTime[:2]
#         min = targetTime[3:5]
#         sec = targetTime[6:8]
#         return (hrs,min,sec)
#     else:
#         return(None,None,None)

# def scheduleJob(data):
#     print("Added request to scheduler ",data.data)
#     r_data = data.data
#     diagID = r_data['diagID'] if "diagID" in r_data else 0
#     starttime = r_data['starttime'] if "starttime" in r_data else None
#     endtime = r_data['endtime'] if "endtime" in r_data else None
#     cmd = r_data['command'] if "command" in r_data else None
#     jobtype = r_data['jobtype'] if "jobtype" in r_data else None
    
#     ## INTERVAL JOB VARIABLES 
#     intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0
#     intv_time = r_data['intv_time'] if "intv_time" in r_data else None
#     intv_hrs, intv_min, intv_sec = timeformatter(intv_time) 

#     ## Add format check for intv_time 

#     # intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
#     # intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
#     # intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
    
    
#     ## CRONJOB VARIABLES
#     # job_month, job_day, job_week, job_dow, job_seconds, job_minutes, job_hours
#     job_month = r_data['job_month'] if "job_month" in r_data else None
#     job_day = r_data['job_day'] if "job_day" in r_data else None
#     job_week = r_data['job_week'] if "job_week" in r_data else None
#     job_year = r_data['job_year'] if "job_year" in r_data else None
#     job_dow = r_data['job_dow'] if "job_dow" in r_data else None
#     job_sec = r_data['job_seconds'] if "job_seconds" in r_data else None
#     job_min = r_data['job_minutes'] if "job_minutes" in r_data else None
#     job_hrs = r_data['job_hours'] if "job_hours" in r_data else None
#     enddate = r_data['enddate'] if "enddate" in r_data else None


#     # start date
#     if diagID == 0 :
#         return ("Diagnostic ID is required", status.HTTP_400_BAD_REQUEST)
#     else:
#         if jobtype == 'date':
#             if starttime != None:
#                 if scheduler.get_job(str(diagID)) == None:
#                     job = scheduler.add_job(sendRequest, trigger='date', run_date=starttime,args=[diagID], id=str(diagID))
#                     return ("Date job scheduled!", status.HTTP_201_CREATED)
#                 elif scheduler.get_job(str(diagID)) != None:
#                     return ("Job with Diagnostic ID already exists", status.HTTP_400_BAD_REQUEST )
#             elif starttime == None:
#                 return ("Date field can't be empty for date jobs", status.HTTP_400_BAD_REQUEST)

#         elif jobtype == 'interval':
#             # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
            
#             if starttime != None and intv_sec != None and intv_hrs != None and intv_min != None :
#                 if scheduler.get_job(str(diagID)) == None:
#                     job = scheduler.add_job(sendRequest, trigger='interval',
#                                         seconds=int(intv_sec),
#                                         minutes=int(intv_min),
#                                         hours = int(intv_hrs),
#                                         weeks = intv_weeks,
#                                         start_date=starttime,
#                                         id=str(diagID), args=[diagID],
#                                         replace_existing=True)
                    
#                     return ("Interval job scheduled!", status.HTTP_201_CREATED)
#                 elif scheduler.get_job(str(diagID)) != None:
#                     return ("Job with diagnostic ID already exists", status.HTTP_400_BAD_REQUEST)
#             elif starttime == None:
#                 return ("Startdate is required for scheduling!", status.HTTP_400_BAD_REQUEST)
#             else:
#                 return ("Error in scheduling job", status.HTTP_400_BAD_REQUEST)

#             # return "job details: %s" % job

#         elif jobtype == 'cron':
#             # hour,min,sec -> int // year,month,day,week,dayofweek
#             if starttime != None:
#                 if scheduler.get_job(str(diagID)) == None:
#                     job = scheduler.add_job(sendRequest, trigger='cron',
#                                         year=job_year,
#                                         month=job_month, 
#                                         day=job_day, 
#                                         week=job_week,
#                                         day_of_week=job_dow,
#                                         hour=job_hrs,
#                                         minute=job_min,
#                                         second=job_sec,
#                                         start_date=starttime,
#                                         end_date=enddate,
#                                         id=str(diagID), args=[diagID],
#                                         replace_existing=True)
#                     return ("Cron job scheduled!", status.HTTP_201_CREATED)
#                 elif scheduler.get_job(str(diagID)) != None:
#                     return ("Job with diagnostic ID already exists", status.HTTP_400_BAD_REQUEST)
#             elif starttime == None:
#                 return ("Specify a startdate", status.HTTP_400_BAD_REQUEST)


   